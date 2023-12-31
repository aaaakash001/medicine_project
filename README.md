# DocAssist Portal

## Project Description

The Medicine Project is organized into the following components:

- **Admin Dashboard**: The `admin_dashboard` directory contains code for an admin dashboard where administrators can manage medicine data and perform administrative tasks.

- **Styling**: The `style` directory holds files for styling the project's user interface.

- **Templates**: The `templates` directory includes templates used for rendering data and information in the admin dashboard.

- **Data Files**: The project uses data files like `.medicine_all.csv.icloud` to store and manage medicine-related information.

- **Composition Calculation**: The `composition.py` script contains all flask framework and dash(plotly framework) codes which is entry point to route to other web pages.

## Project File Structure

```txt
project/
│
├── backend/ (Flask Backend)
│   ├── app.py (contains flask and dash code)
│   ├── static/ (contains javascript and css file)
│   │   ├── admin_dashboard.css
│   │   ├── admin_dashboard_script.js
│   │   ├── admin_script.js
│   │   ├── analysis_script.js
│   │   ├── bill_script.js
│   │   ├── prescription_script.js
│   │   ├── brand_script.js
│   │   └── script.js
│   └── templates/ (contains html files)
│       ├── index.html
│       ├── admin_dashboard.html
│       ├── admin.html
│       ├── analysis.html
│       ├── bill.html
│       ├── brands.html
│       ├── prescription.html
│       └── results.html
│
├── database/ (PostgreSQL Volume)
│   ├── postgresdb
│   └── queries/
│
├── scrapers/ (Scripts for scraping)
│   ├── 1mg.py
│   └── data/
│       └── 1mg/
│           ├── all_medicines.csv
│           └── medicines-by-alphabet/
│               ├── medicine_dataA.csv
│               ├── medicine_dataB.csv
│               ├── ...
│               └── medicine_dataZ.csv
└── docs/
    └── proposal.pdf

```

## Getting Started

Set the environment

.env file should contain following variables defined:

```txt
DB_PROTOCOL="postgresql"
DB_HOST="localhost"
DB_PORT="5432"
DB_USER="docassist"
DB_PASSWORD="aakashchaitanya"
DB_NAME="medicine"
```

Also look for environment variables in docker-compose.yml

To start database

```sh
docker-compose up
```

To start backend server

```sh
cd backend
python app.py
```

## Developers

- Use Camel case for defining variables
- Use Snake case for defining functions
- Use Pascal case for defining class names

## Contributors

- Aakash Agrawal
- Chaitanya Shinge
