##! /usr/bin/python3
import logging
import os
import sys
#from getpass import getpass
#from optparse import OptionParser
#from configobj import ConfigObj
import configparser


from attachment_downloader.attachment_downloader import AttachmentDownloader

if __name__ == '__main__':
    print(os.getcwd())
    attach_config = configparser.ConfigParser()
    attach_config.read("\\test_config.ini")
    imap_host =attach_config['imap']['host']
    imap_user = attach_config['imap']['username']
    imap_password = attach_config['imap']['password']
    imap_folder = attach_config['imap']['folder']
    download_folder = attach_config['local']['folder']

    std_out_stream_handler = logging.StreamHandler(sys.stdout)
    std_out_stream_handler.setLevel(logging.DEBUG)
    std_out_stream_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(std_out_stream_handler)


    downloader = AttachmentDownloader(imap_host)

    logging.info("Logging in to: '%s' as '%s'", imap_host, imap_user)
    downloader.login(imap_user, imap_password)

    logging.info("Listing messages folder folder: %s", imap_folder)
    messages = downloader.list_messages(imap_folder)

    print("Message list")
    print(len(messages))
    for message in messages:
        print(message.to_address)
        myfolder=message.to_address.split("@")[0].split("+")
        print(myfolder[0])
        print(len(myfolder))
        i=2
        #First one is always email address, second one Cabinet.
        new_download_folder=download_folder
        while i < len(myfolder):
            new_download_folder=os.path.join(new_download_folder,myfolder[i])
            if not os.path.exists(new_download_folder):
                os.makedirs(new_download_folder)
            i=i+1
        print(new_download_folder)
        for attachment_name in message.list_attachments():
            print(new_download_folder)
            print(attachment_name)
            download_filename = os.path.join(new_download_folder, attachment_name)
            logging.info("Downloading attachment '%s' for message '%s': %s", attachment_name, message.subject,
                         download_filename)
            fp = open(download_filename, 'wb')
            fp.write(message.get_attachment_payload(attachment_name))
            fp.close()
    logging.info('Finished processing messages')

    logging.info('Logging out of: %s', imap_host)
    downloader.logout()

    logging.info("Done")
