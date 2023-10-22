import re
import pandas as pd
from translate_message import pt
import os
import tqdm
import csv

log_file_path = '../datasets/casper-rw/logs/'

log_pattern = {
    "auth" : {
        "file": "auth.log",
        "pattern_priority": [
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.+?)\s+(.+?):\s+.*?\w*?:\s(.*?)$',
                "group": ['timestamp', 'hostname', 'service', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.+?)\s+(.+?):\s+(.*?)$',
                "group": ['timestamp', 'hostname', 'service', 'message_part']
            },
            # {
            #     "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(\w+)\s(.*):\s(.*)$',
            #     "group": ['timestamp', 'hostname', 'service', 'message_part']
            # },
        ] 
    },
    "daemon" : {
        "file": "daemon.log",
        "pattern_priority": [
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s+(.*)$',
                "group": ['timestamp', 'hostname', 'service', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*)$',
                "group": ['timestamp', 'hostname', 'message_part']
            }
        ]
    },
    "debug" : {
        "file": "debug",
        "pattern_priority": [
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s\[\s+\d+.\d+\]\s+(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s+(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            }
        ]
    },
    "dmesg" : {
        "file": "dmesg",
        "pattern_priority": [
            {
                "pattern": r'^\[\s+(\d+.\d+)]\s(.*)$',
                "group": ['timestamp', 'message_part']
            },
            {
                "pattern": r'^(.*)$',
                "group": ['message_part']
            }
        ]
    },
    "messages" : {
        "file": "messages",
        "pattern_priority": [
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s\[\s+\d+.\d+]\s(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*)$',
                "group": ['timestamp', 'hostname', 'message_part']
            }
        ]
    },
    "syslog" : {
        "file": "syslog",
        "pattern_priority": [
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s\[\s+\d+.\d+]\s(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*)$',
                "group": ['timestamp', 'hostname', 'message_part']
            }
        ]
    },
    "kern" : {
        "file": "kern.log",
        "pattern_priority": [
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s\[\s+\d+.\d+]\s(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*?):\s(.*)$',
                "group": ['timestamp', 'hostname', 'log_source', 'message_part']
            },
            {
                "pattern": r'^(\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2})\s(.*?)\s(.*)$',
                "group": ['timestamp', 'hostname', 'message_part']
            }
        ]
    },
    
}

def get_auth_log_messages(log_file_path, pattern_priority, output_log_file_path):
    # auth_messages = []
    # prepare output log file
    output_log_file = open(output_log_file_path, 'a')
    output_log_writer = csv.writer(output_log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # write header: timestamp, message
    output_log_writer.writerow(['timestamp', 'message', 'source'])

    total_line = sum(1 for line in open(log_file_path, 'r'))
    progress_bar = tqdm.tqdm(total=total_line, desc="Processing log file", unit="line")

    with open(log_file_path, 'r') as log_file:
        line_number = 0
        for line in log_file:
            for pattern in pattern_priority:
                match = re.match(pattern['pattern'], line)
                if match:
                    match_groups = match.groups()

                    timestamp = match_groups[pattern['group'].index('timestamp')] if 'timestamp' in pattern['group'] else None
                    hostname = match_groups[pattern['group'].index('hostname')] if 'hostname' in pattern['group'] else None
                    service = match_groups[pattern['group'].index('service')] if 'service' in pattern['group'] else None
                    message_part = match_groups[pattern['group'].index('message_part')]

                    # clean message
                    message = message_part.strip()
                    # translate message
                    translated_message = translate_message(message, pt)

                    write_message = translated_message if translated_message else message

                    # write to output log file
                    output_log_writer.writerow([timestamp, write_message, log_file_path])
                    progress_bar.update(1)
                    line_number += 1
                    break

                if not match and pattern == pattern_priority[-1]:
                    print(f"NOT MATCH: {line_number} :: {line}")
                    exit()

    output_log_file.close()

    # return auth_messages
    
def translate_message(message, pattern_table):
    for pattern in pattern_table:
        match = re.match(pattern['pattern'], message)
        if match:
            template = pattern['template']
            translated_message = template
            for i, group in enumerate(match.groups()):
                translated_message = translated_message.replace("{!" + str(i+1) + "!}", group)

            return translated_message
    return None

if __name__ == '__main__':
    dataset_list = [
        "casper-rw",
        "dfrws-2009-jhuisi",
        "dfrws-2009-nssal",
        "honeynet-challenge7",
        "honeynet-challenge5",
    ]

    for dataset in dataset_list:
        print("="*50)
        print(f"Dataset: {dataset}")

        output_dir = f'../output/{dataset}'
        log_file_path = f'../datasets/{dataset}/logs/'

        # create output directory if not exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        merge_output_path = f'../output/{dataset}.csv'

        total_messages = 0
        for log_type, info in log_pattern.items():
            log_file = info['file']
            pattern_priority = info['pattern_priority']
            print("="*50)
            print(f"Log file: {log_file}")

            file_part = -1
            while True:
                log_file_name = log_file
                # check for possible log file division
                if file_part >= 0:
                    log_file_name = f"{log_file}.{file_part}"
                try:
                    with open(log_file_path + log_file_name, 'r') as f:
                        pass
                    file_part += 1
                except FileNotFoundError:
                    break

                get_auth_log_messages(log_file_path + log_file_name, pattern_priority, merge_output_path)

        print("="*50)