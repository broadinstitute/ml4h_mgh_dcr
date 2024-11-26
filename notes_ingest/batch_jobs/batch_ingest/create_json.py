import json

# File containing the JSON template
template_file = 'template.json'

base_http = "https://ml4h.blob.core.windows.net/mgh-data-lake/"
sas = "?" # Insert here a SAS token that has read/write/create/list permission

notes_file_types = ['Car', 'End', 'Pul', 'Hnp', 'Opn', 'Rad', 'Dis', 'Mic', 'Pat', 'Trn', 'Lno', 'Vis', 'Prg']

chunk_list = ["JH59_20240126_092101",
              "JH59_20240126_092647",
              "JH59_20240126_094230",
              "JH59_20240126_094725",
              "JH59_20240126_095015",
              "JH59_20240126_095309",
              "JH59_20240126_095614",
              "JH59_20240126_095906",
              "JH59_20240126_100200",
              "JH59_20240126_100446",
              "JH59_20240126_100803",
              "JH59_20240126_101056",
              "JH59_20240126_101320",
              "JH59_20240126_101616",
              "JH59_20240126_103507",
              "JH59_20240126_103756",
              "JH59_20240126_104034",
              "JH59_20240126_104455",
              "JH59_20240126_104811",
              "JH59_20240126_105032"]

for id, chunk in enumerate(chunk_list):
    # Given id and resourceFiles
    id_value = chunk  # Replace with your actual ID

    output_blob_prefix = base_http + "pclc/phi_min/ingested/"
    outputFiles = [
        {
            "filePattern": "/data/output/*",
            "destination": {
                "container": {
                    "containerUrl": output_blob_prefix + sas
                }
            },
            "uploadOptions": {
                "uploadCondition": "TaskSuccess"
            }
        },
        {
            "filePattern": "stdout",
            "destination": {
                "container": {
                    "containerUrl": output_blob_prefix + chunk + "/" + sas
                }
            },
            "uploadOptions": {
                "uploadCondition": "TaskCompletion"
            }
        },
        {
            "filePattern": "stderr",
            "destination": {
                "container": {
                    "containerUrl": output_blob_prefix + chunk + "/" + sas
                }
            },
            "uploadOptions": {
                "uploadCondition": "TaskCompletion"
            }
        }
    ]

    # Input all the resource files
    resourceFiles = []

    for t in notes_file_types:
        file_name = chunk + "_" + t + "_cleaned.txt"
        t_str = base_http + "pclc/phi_min/raw/" + chunk + "/" + file_name + sas
        resourceFiles.append({"httpUrl": t_str, "filePath": "/data/input/" + file_name})

    # Read the JSON template from the file
    with open(template_file, 'r') as f:
        template = json.load(f)

    # Fill in the template
    template["id"] = id_value
    template["resourceFiles"] = resourceFiles
    template["outputFiles"] = outputFiles

    # Output the completed JSON
    output_file = "./jsons/" + chunk + ".json"
    with open(output_file, 'w') as f:
        json.dump(template, f, indent=2)

