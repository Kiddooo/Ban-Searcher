# Top

<img src="https://raw.githubusercontent.com/PKief/vscode-material-icon-theme/ec559a9f6bfd399b82bb44393651661b08aaf7ba/icons/folder-markdown-open.svg" width="100" />

## ◦ Developed with the software and tools below

![GNU Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=for-the-badge&logo=GNU-Bash&logoColor=white)
![YAML](https://img.shields.io/badge/YAML-CB171E.svg?style=for-the-badge&logo=YAML&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=Python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000.svg?style=for-the-badge&logo=Flask&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032.svg?style=for-the-badge&logo=Git&logoColor=white)

---

## 📖 Table of Contents

- [🔝 Top](#top)
- [📖 Table of Contents](#-table-of-contents)
- [📍 Overview](#-overview)
- [📦 Features](#-features)
- [📂 repository Structure](#-repository-structure)
- [⚙️ Modules](#modules)
- [🚀 Getting Started](#-getting-started)
  - [🔧 Installation](#-installation)
  - [🤖 Running ](#-running-)
  - [🧪 Tests](#-tests)
- [🛣 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [👏 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

Ban-Searcher is a Python-based project designed to search for bans across various platforms. It utilizes Python and JSON technologies to effectively parse and analyze ban data. The project is organized into several Python scripts for different websites, each script tailored to the specific structure and requirements of the respective website.

The main entry point of the project is `project.py`, which coordinates the execution of the different scripts and manages the overall workflow.

## The project is designed with extensibility in mind, allowing for the addition of new website scripts as needed. This makes Ban-Searcher a versatile tool for anyone looking to gather and analyze ban data across multiple platforms.

## 📦 Features

Ban-Searcher offers the following key features:

1. **Extensive Ban Search**: Ban-Searcher can search for bans across multiple platforms, providing a comprehensive view of ban data.

2. **Website-Specific Scripts**: The project includes Python scripts tailored to different websites, ensuring accurate and efficient data retrieval.

3. **Extensibility**: The project is designed with extensibility in mind, allowing for the addition of new website scripts as needed.

4. **Versatility**: Ban-Searcher is a versatile tool that can be used by anyone looking to gather and analyze ban data across multiple platforms.

---

## 📂 Repository Structure

```sh
└── /
    ├── .env_copy
    ├── banlist_project/
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders/
    │       ├── banmanager_bonemeal_spider.py
    │       ├── banmanager_spider.py
    │       ├── cosmicgames_spider.py
    │       ├── cubeville_spider.py
    │       ├── cultcraft_spider.py
    │       ├── democracycraft_spider.py
    │       ├── guster_spider.py
    │       ├── johnymuffin_spider.py
    │       ├── litebans_spider.py
    │       ├── majncraft_spider.py
    │       ├── manacube_spider.py
    │       ├── mcbans_spider.py
    │       ├── mcbouncer_spider.py
    │       ├── mcbrawl_spider.py
    │       ├── mccentral_spider.py
    │       ├── mconline_spider.py
    │       ├── mundominecraft_spider.py
    │       ├── snapcraft_spider.py
    │       ├── strongcraft_spider.py
    │       ├── syuu_spider.py
    │       └── uhc_ubl.py
    ├── player_converter.py
    ├── player_report.py
    ├── project.py
    ├── requirements.txt
    ├── start.bat
    ├── start.sh
    └── utils.py

```

---

## ⚙️ Modules

<details closed><summary>Root</summary>

| File                     | Summary                                                                                                                                  |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------- |
| [start.sh](#)            | This script starts the application.                                                                                                      |
| [project.py](#)          | This is the main entry point of the application. It coordinates the execution of the different scripts and manages the overall workflow. |
| [.env_copy](#)           | This file contains environment variables needed for the project.                                                                         |
| [requirements.txt](#)    | This file lists the Python dependencies that need to be installed for the project to run.                                                |
| [player_report.py](#)    | This script generates reports for players.                                                                                               |
| [player_converter.py](#) | This script converts player data into a desired format.                                                                                  |
| [utils.py](#)            | This module contains utility functions that are used across the project.                                                                 |
| [start.bat](#)           | This script starts the application on Windows systems.                                                                                   |

</details>

<details closed><summary>Banlist_project</summary>

| File                | Summary                                                          |
| ------------------- | ---------------------------------------------------------------- |
| [pipelines.py](#)   | This script manages data pipelines in the project.               |
| [items.py](#)       | This script defines the data items that the spiders will return. |
| [middlewares.py](#) | This script handles requests made by the spiders.                |
| [settings.py](#)    | This script contains settings for the Scrapy spiders.            |

</details>

<details closed><summary>Spiders</summary>

| File                                                                                     | Summary                                                                        |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| File                                                                                     | Summary                                                                        |
| ----------------------------------                                                       | ------------------------------------------------------------------------------ |
| [banmanager_bonemeal_spider.py](./banlist_project/spiders/banmanager_bonemeal_spider.py) | This spider is tailored to search for bans on the BanManager BoneMeal website. |
| [banmanager_spider.py](./banlist_project/spiders/banmanager_spider.py)                   | This spider is tailored to search for bans on the BanManager website.          |
| [cosmicgames_spider.py](./banlist_project/spiders/cosmicgames_spider.py)                 | This spider is tailored to search for bans on the CosmicGames website.         |
| [cubeville_spider.py](./banlist_project/spiders/cubeville_spider.py)                     | This spider is tailored to search for bans on the Cubeville website.           |
| [cultcraft_spider.py](./banlist_project/spiders/cultcraft_spider.py)                     | This spider is tailored to search for bans on the CultCraft website.           |
| [democracycraft_spider.py](./banlist_project/spiders/democracycraft_spider.py)           | This spider is tailored to search for bans on the DemocracyCraft website.      |
| [guster_spider.py](./banlist_project/spiders/guster_spider.py)                           | This spider is tailored to search for bans on the Guster website.              |
| [johnymuffin_spider.py](./banlist_project/spiders/johnymuffin_spider.py)                 | This spider is tailored to search for bans on the JohnyMuffin website.         |
| [litebans_spider.py](./banlist_project/spiders/litebans_spider.py)                       | This spider is tailored to search for bans on the LiteBans website.            |
| [majncraft_spider.py](./banlist_project/spiders/majncraft_spider.py)                     | This spider is tailored to search for bans on the Majncraft website.           |
| [manacube_spider.py](./banlist_project/spiders/manacube_spider.py)                       | This spider is tailored to search for bans on the ManaCube website.            |
| [mcbans_spider.py](./banlist_project/spiders/mcbans_spider.py)                           | This spider is tailored to search for bans on the MCBans website.              |
| [mcbouncer_spider.py](./banlist_project/spiders/mcbouncer_spider.py)                     | This spider is tailored to search for bans on the MCBouncer website.           |
| [mcbrawl_spider.py](./banlist_project/spiders/mcbrawl_spider.py)                         | This spider is tailored to search for bans on the MCBrawl website.             |
| [mccentral_spider.py](./banlist_project/spiders/mccentral_spider.py)                     | This spider is tailored to search for bans on the MCCentral website.           |
| [mconline_spider.py](./banlist_project/spiders/mconline_spider.py)                       | This spider is tailored to search for bans on the MCOnline website.            |
| [mundominecraft_spider.py](./banlist_project/spiders/mundominecraft_spider.py)           | This spider is tailored to search for bans on the MundoMinecraft website.      |
| [snapcraft_spider.py](./banlist_project/spiders/snapcraft_spider.py)                     | This spider is tailored to search for bans on the SnapCraft website.           |
| [strongcraft_spider.py](./banlist_project/spiders/strongcraft_spider.py)                 | This spider is tailored to search for bans on the StrongCraft website.         |
| [syuu_spider.py](./banlist_project/spiders/syuu_spider.py)                               | This spider is tailored to search for bans on the Syuu website.                |
| [uhc_ubl.py](./banlist_project/spiders/uhc_ubl.py)                                       | This spider is tailored to search for bans on the UHC UBL website.             |

## </details>

## 🚀 Getting Started

**_Dependencies_**

Please ensure you have the following dependencies installed on your system:

`- beautifulsoup4==4.12.2`
`- dateparser==1.2.0`
`- deep_translator==1.11.4`
`- Flask==3.0.0`
`- google_api_python_client==2.111.0`
`- InquirerPy==0.3.4`
`- protobuf==3.18.3`
`- pydantic==2.5.3`
`- python-dotenv==1.0.0`
`- Requests==2.31.0`
`- Scrapy==2.11.0`
`- tldextract==3.1.2`

### 🔧 Installation

1. Clone the Ban-Searcher repository:

```sh
git clone https://github.com/Kiddooo/Ban-Searcher.git
```

2. Navigate to the project directory:

```sh
cd Ban-Searcher
```

3. Initialize and update the Git submodules:

```sh
git submodule init
git submodule update
```

4. Install the dependencies:

```sh
pip install -r requirements.txt
```

### 🤖 Running

```sh
# For Linux/Mac
python3 project.py

# For Windows
py project.py
```

## 🛣 Project Roadmap

> - [ ] `ℹ️  Task 1: Implement more sources`
> - [ ] `ℹ️  Task 2: Implement better code`
> - [ ] `ℹ️ ...`

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](./CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/Kiddooo/Ban-Searcher/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github.com/Kiddooo/Ban-Searcher/issues)**: Submit bugs found or log feature requests for Ban-Searcher.

#### _Contributing Guidelines_

<details closed>
<summary>Click to expand</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.

```sh
git clone <your-forked-repo-url>
```

3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.

```sh
git checkout -b new-feature-x
```

4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear and concise message describing your updates.

```sh
git commit -m 'Implemented new feature x.'
```

6. **Push to GitHub**: Push the changes to your forked repository.

```sh
git push origin new-feature-x
```

7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

## </details>

## 📄 License

## This project is protected under the [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html). For more details, refer to the [LICENSE](https://github.com/Kiddooo/Ban-Searcher/blob/main/LICENSE.md) file.

## 👏 Acknowledgments

- 105hua: For their useful insight and feedback.

[**Return**](#Top)

---
