<p align="center">
  <img src="https://img.icons8.com/pulsar-color/96/markdown.png" width="100" />
</p>
<p align="center">
    <h1 align="center">BAN-SEARCHER</h1>
</p>
<p align="center">
    <em>Unmask Players, Enforce Fair Play!</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/Kiddooo/Ban-Searcher?style=flat&color=0080ff" alt="license">
	<img src="https://img.shields.io/github/last-commit/Kiddooo/Ban-Searcher?style=flat&color=0080ff" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/Kiddooo/Ban-Searcher?style=flat&color=0080ff" alt="repo-top-language">
	<img src="https://img.shields.io/github/languages/count/Kiddooo/Ban-Searcher?style=flat&color=0080ff" alt="repo-language-count">
<p>
<p align="center">
		<em>Developed with the software and tools below.</em>
</p>
<p align="center">
	<img src="https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white" alt="GNU%20Bash">
	<img src="https://img.shields.io/badge/HTML5-E34F26.svg?style=flat&logo=HTML5&logoColor=white" alt="HTML5">
	<img src="https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white" alt="Python">
	<img src="https://img.shields.io/badge/Flask-000000.svg?style=flat&logo=Flask&logoColor=white" alt="Flask">
</p>
<hr>

## 🔗 Quick Links

> - [📍 Overview](#-overview)
> - [📦 Features](#-features)
> - [📂 Repository Structure](#-repository-structure)
> - [🧩 Modules](#-modules)
> - [🚀 Getting Started](#-getting-started)
>   - [⚙️ Installation](#️-installation)
>   - [🤖 Running Ban-Searcher](#-running-ban-searcher)
> - [🛠 Project Roadmap](#-project-roadmap)
> - [🤝 Contributing](#-contributing)
> - [📄 License](#-license)
> - [👏 Acknowledgments](#-acknowledgments)

---

## 📍 Overview

Ban-Searcher is a specialized tool for querying Minecraft player bans. It leverages Detect Language API to analyze text and Mojang's API to convert player usernames to UUIDs. The project's value lies in its ability to streamline the process of tracking banned players, aiding server administrators in maintaining fair play and community standards. Real-world utility is enhanced through language detection for international servers, thus broadening the potential user base.

---

## 📦 Features

|    | Feature           | Description                                                                 |
|----|-------------------|-----------------------------------------------------------------------------|
| ⚙️  | **Architecture**  | The project is a modular web scraping tool using Python and Scrapy.         |
| 🔩 | **Code Quality**  | Code appears to be clean, with PEP8 adherence and use of Pythonic idioms.   |
| 📄 | **Documentation** | Limited in-line comments; no explicit usage docs or comments on functions.  |
| 🔌 | **Integrations**  | Integrates with various web services for data scraping and language APIs.   |
| 🧩 | **Modularity**    | Code is divided into spiders, models, and utility scripts for reusability.  |
| 🧪 | **Testing**       | No mention of testing frameworks; testing strategy is not evident.          |
| ⚡️  | **Performance**   | Performance will depend on the scraping efficiency and third-party services.|
| 🛡️ | **Security**      | Uses .env for API keys; specific security measures are not detailed.        |
| 📦 | **Dependencies**  | Uses Scrapy, Requests, BeautifulSoup, Pydantic, Flask, and other libraries.|
| 🚀 | **Scalability**   | Scalability is not addressed; may need optimization for high load.          |


---

## 📂 Repository Structure

```sh
└── Ban-Searcher/
    ├── .env_copy
    ├── banlist_project
    │   ├── items.py
    │   ├── middlewares.py
    │   ├── pipelines.py
    │   ├── settings.py
    │   └── spiders
    │       ├── banmanager_bonemeal_spider.py
    │       ├── banmanager_spider.py
    │       ├── cosmicgames_spider.py
    │       ├── cubeville_spider.py
    │       ├── cultcraft_spider.py
    │       ├── democracycraft_spider.py
    │       ├── google_sheets.py
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
    │       └── syuu_spider.py
    ├── player_converter.py
    ├── player_report.py
    ├── project.py
    ├── report
    │   ├── report.py
    │   └── templates
    │       └── index.html
    ├── requirements.txt
    ├── start.bat
    ├── start.sh
    └── utils.py
```

---

## 🧩 Modules

<details closed><summary>.</summary>

| File                                                                                           | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---                                                                                            | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| [.env_copy](https://github.com/Kiddooo/Ban-Searcher/blob/master/.env_copy)                     | The `.env_copy` file stores a template for environment variables, specifically the API key for a language detection service, used across the `Ban-Searcher` repository, likely for internationalization support in the web scraping modules. |
| [player_converter.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/player_converter.py) | This codebase is for the Ban-Searcher project, focused on scraping and generating reports on player bans from various gaming servers. The structure indicates a Scrapy framework with multiple spiders tailored to different servers, integration with Google Sheets, and facilities for reporting and converting player data.Summary:Centralized ban monitoring and reporting tool for gaming communities; leverages web scraping to aggregate server ban data. |
| [player_report.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/player_report.py)       | The codebase is for a scraping tool designed to extract ban data from various gaming communities, likely to monitor or analyze player bans. The spiders collect ban information, which is processed and potentially reported or integrated with external systems. |
| [requirements.txt](https://github.com/Kiddooo/Ban-Searcher/blob/master/requirements.txt)       | The Ban-Searcher repository leverages Scrapy for data collection, with Flask for web reporting, and interacts with Google Sheets API for data storage and retrieval. It's designed for tracking ban records across various game servers. |
| [utils.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/utils.py)                       | The code is part of a Scrapy-based project designed to scrape ban information from various gaming servers, then process and integrate this data into a centralized system for reporting and analysis. |
| [project.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/project.py)                   | The code snippet is part of a Scrapy project that aggregates ban data from various gaming servers. The `Ban-Searcher` repository primarily consists of multiple spiders for different servers, data processing pipelines, and reporting tools, aimed at tracking player bans in an online gaming community. |
| [start.bat](https://github.com/Kiddooo/Ban-Searcher/blob/master/start.bat)                     | The `start.bat` file is an entry-point script for initializing the Ban-Searcher application on Windows systems. |
| [start.sh](https://github.com/Kiddooo/Ban-Searcher/blob/master/start.sh)                       | The `start.sh` file is an entry-point script for initializing the Ban-Searcher application on Unix |

</details>

<details closed><summary>banlist_project</summary>

| File                                                                                                 | Summary                                                                                                                                                                                                                                      |
| ---                                                                                                  | ---                                                                                                                                                                                                                                          |
| [pipelines.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/pipelines.py)     | The `pipelines.py` defines `BanPipeline` for processing banned player data in a web crawling framework, managing initialization and item processing.                                                                                         |
| [middlewares.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/middlewares.py) | The code snippet is middleware for a web scraping framework, responsible for handling requests and responses within a system designed to aggregate online gaming ban records.                                                                |
| [settings.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/settings.py)       | This configuration establishes settings for a web scraping project that disables logging, sets timeouts, user agents, and manages concurrent requests, middleware, pipelines, and performance features like auto-throttling and DNS caching. |
| [items.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/items.py)             | Defines the BanItem model |

</details>

<details closed><summary>banlist_project.spiders</summary>

| File                                                                                                                                       | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                                                                        | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [majncraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/majncraft_spider.py)                     | This spider (`MajncraftSpider`) scrapes player ban data from Majncraft and yields translated ban items for the Ban-Searcher  |
| [litebans_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/litebans_spider.py)                       | This spider (`LiteBansSpider`) scrapes player ban data from various server websites running LiteBans and yields translated ban items for the Ban-Searcher  |
| [mconline_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mconline_spider.py)                       | This spider (`MCOnlineSpider`) scrapes player ban data from the MCOnline API and yields translated ban items for the Ban-Searcher  |
| [mcbans_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mcbans_spider.py)                           | This spider (`MCBansSpider`) scrapes player ban data from MCBans and yields translated ban items for the Ban-Searcher  |
| [banmanager_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/banmanager_spider.py)                   | This spider (`BanManagerSpider`) scrapes player ban data from various servers running BanManager and yields translated ban items for the Ban-Searcher  |
| [banmanager_bonemeal_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/banmanager_bonemeal_spider.py) | This spider (`BanManagerBonemealSpider`) scrapes player ban data from servers running BanManager-Bonemeal and yields translated ban items for the Ban-Searcher  |
| [strongcraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/strongcraft_spider.py)                 | This spider (`StrongcraftSpider`) scrapes player ban data from Strongcraft and yields translated ban items for the Ban-Searcher  |
| [johnymuffin_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/johnymuffin_spider.py)                 | This spider (`JohnyMuffinSpider`) scrapes player ban data from JohnyMuffin and yields translated ban items for the Ban-Searcher  |
| [guster_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/guster_spider.py)                           | This spider (`GusterSpider`) scrapes player ban data from Guster and yields translated ban items for the Ban-Searcher  |
| [syuu_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/syuu_spider.py)                               | This spider (`SyuuSpider`) scrapes player ban data from Syuu and yields translated ban items for the Ban-Searcher  |
| [cultcraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/cultcraft_spider.py)                     | This spider (`CultCraftSpider`) scrapes player ban data from CultCraft and yields translated ban items for the Ban-Searcher  |
| [cosmicgames_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/cosmicgames_spider.py)                 | This spider (`CosmicGamesSpider`) scrapes player ban data from Cosmic Games' API and yields translated ban items for the Ban-Searcher  |
| [mundominecraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mundominecraft_spider.py)           | This spider (`MundoMinecraftSpider`) scrapes player ban data from MundoMinecraft and yields translated ban items for the Ban-Searcher  |
| [cubeville_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/cubeville_spider.py)                     | This spider (`CubevilleSpider`) scrapes player ban data from Cubeville and yields translated ban items for the Ban-Searcher  |
| [manacube_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/manacube_spider.py)                       | This spider (`ManaCubeSpider`) scrapes player ban data from ManaCube and yields translated ban items for the Ban-Searcher  |
| [mcbouncer_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mcbouncer_spider.py)                     | This spider (`MCBouncerSpider`) scrapes player ban data from MCBouncer and yields translated ban items for the Ban-Searcher  |
| [google_sheets.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/google_sheets.py)                           | This spider (`GoogleSheetsSpider`) scrapes player ban data from the UHC UBL Sheet and yields translated ban items for the Ban-Searcher  |
| [snapcraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/snapcraft_spider.py)                     | This spider (`SnapcraftSpider`) scrapes player ban data from Snapcraft and yields translated ban items for the Ban-Searcher  |
| [democracycraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/democracycraft_spider.py)           | This spider (`DemocracyCraftSpider`) scrapes player ban data from DemocracyCraft and yields translated ban items for the Ban-Searcher  |
| [mcbrawl_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mcbrawl_spider.py)                         | This spider (`MCBrawlSpider`) scrapes player ban data from MCBrawl and yields translated ban items for the Ban-Searcher  |
| [mccentral_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mccentral_spider.py)                     | This spider (`MCCentralSpider`) scrapes player ban data from MCCentral and yields translated ban items for the Ban-Searcher  |

</details>

<details closed><summary>report</summary>

| File                                                                              | Summary                                                                                                                                               |
| ---                                                                               | ---                                                                                                                                                   |
| [report.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/report/report.py) | The `report.py` serves as a Flask web application within the Ban-Searcher repo, providing a web interface to display ban reports. |

</details>

<details closed><summary>report.templates</summary>

| File                                                                                          | Summary                                                                                                                                                                          |
| ---                                                                                           | ---                                                                                                                                                                              |
| [index.html](https://github.com/Kiddooo/Ban-Searcher/blob/master/report/templates/index.html) | The HTML for the web interface. |

</details>

---

## 🚀 Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `3.12`
* **FlareSolverr**: [FlareSolverr](https://github.com/FlareSolverr/FlareSolverr)

### ⚙️ Installation

1. Clone the Ban-Searcher repository:

```sh
git clone https://github.com/Kiddooo/Ban-Searcher
```

2. Change to the project directory:

```sh
cd Ban-Searcher
```

3. Install the dependencies:

```sh
pip install -r requirements.txt
```
4. Modify .env file:
```sh
mv .env_copy .env
```

### 🤖 Running Ban-Searcher

Use the following command to run Ban-Searcher:

```sh
python main.py
```

---

## 🛠 Project Roadmap

- [ ] `► Cleanup and optimize the code`
- [ ] `► Gather more sources`
- [ ] `► ...`

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github.com/Kiddooo/Ban-Searcher/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Report Issues](https://github.com/Kiddooo/Ban-Searcher/issues)**: Submit bugs found or log feature requests for Ban-searcher.

<details closed>
    <summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your GitHub account.
2. **Clone Locally**: Clone the forked repository to your local machine using a Git client.
   ```sh
   git clone https://github.com/Kiddooo/Ban-Searcher
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to GitHub**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.

Once your PR is reviewed and approved, it will be merged into the main branch.

</details>

---

## 📄 License

This project is protected under the [AGPL-3.0](https://choosealicense.com/licenses/agpl-3.0/) License. For more details, refer to the [LICENSE](https://github.com/Kiddooo/Ban-Searcher/blob/main/LICENSE.md) file.

---

## 👏 Acknowledgments

- 105hua: Development of the WebUI.

[**Return**](#-quick-links)

---
