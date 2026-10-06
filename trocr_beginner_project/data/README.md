# Data

Large research datasets are not stored in this repository.

## IAM Handwriting Database

IAM is used for handwritten text recognition experiments.

Download the dataset from the official IAM Handwriting Database website:

https://fki.tic.heia-fr.ch/databases/iam-handwriting-database

Expected local structure:

data/iam/
├── ascii/
├── lines/
├── xml/
└── splits/

The `data/iam/` directory is excluded from Git using `.gitignore`.

After downloading and extracting IAM, generate the project manifest using:

python3 -m src.create_iam_sample