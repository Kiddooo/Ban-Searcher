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
>   - [🤖 Running Ban-Searcher](#-running-Ban-Searcher)
>   - [🧪 Tests](#-tests)
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
| [.env_copy](https://github.com/Kiddooo/Ban-Searcher/blob/master/.env_copy)                     | The `.env_copy` file stores a template for environment variables, specifically the API key for a language detection service, used across the `Ban-Searcher` repository, likely for internationalization support in the web scraping modules.                                                                                                                                                                                                                     |
| [player_converter.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/player_converter.py) | This codebase is for the Ban-Searcher project, focused on scraping and generating reports on player bans from various gaming servers. The structure indicates a Scrapy framework with multiple spiders tailored to different servers, integration with Google Sheets, and facilities for reporting and converting player data.Summary:Centralized ban monitoring and reporting tool for gaming communities; leverages web scraping to aggregate server ban data. |
| [start.bat](https://github.com/Kiddooo/Ban-Searcher/blob/master/start.bat)                     | The `start.bat` file is an entry-point script for initializing the Ban-Searcher application on Windows systems.                                                                                                                                                                                                                                                                                                                                                  |
| [player_report.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/player_report.py)       | The codebase is for a scraping tool designed to extract ban data from various gaming communities, likely to monitor or analyze player bans. The spiders collect ban information, which is processed and potentially reported or integrated with external systems.                                                                                                                                                                                                |
| [start.sh](https://github.com/Kiddooo/Ban-Searcher/blob/master/start.sh)                       | The start.sh script serves as an entry point to execute the project.py script, initiating the Ban-Searcher application within its ecosystem.                                                                                                                                                                                                                                                                                                                     |
| [requirements.txt](https://github.com/Kiddooo/Ban-Searcher/blob/master/requirements.txt)       | The Ban-Searcher repository leverages Scrapy for data collection, with Flask for web reporting, and interacts with Google Sheets API for data storage and retrieval. It's designed for tracking ban records across various game servers.                                                                                                                                                                                                                         |
| [utils.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/utils.py)                       | The code is part of a Scrapy-based project designed to scrape ban information from various gaming servers, then process and integrate this data into a centralized system for reporting and analysis.                                                                                                                                                                                                                                                            |
| [project.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/project.py)                   | The code snippet is part of a Scrapy project that aggregates ban data from various gaming servers. The `Ban-Searcher` repository primarily consists of multiple spiders for different servers, data processing pipelines, and reporting tools, aimed at tracking player bans in an online gaming community.                                                                                                                                                      |

</details>

<details closed><summary>banlist_project</summary>

| File                                                                                                 | Summary                                                                                                                                                                                                                                      |
| ---                                                                                                  | ---                                                                                                                                                                                                                                          |
| [pipelines.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/pipelines.py)     | The `pipelines.py` defines `BanPipeline` for processing banned player data in a web crawling framework, managing initialization and item processing.                                                                                         |
| [middlewares.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/middlewares.py) | The code snippet is middleware for a web scraping framework, responsible for handling requests and responses within a system designed to aggregate online gaming ban records.                                                                |
| [settings.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/settings.py)       | This configuration establishes settings for a web scraping project that disables logging, sets timeouts, user agents, and manages concurrent requests, middleware, pipelines, and performance features like auto-throttling and DNS caching. |
| [items.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/items.py)             | Defines BanItem model in a web scraping project, centralizing ban data structure.                                                                                                                                                            |

</details>

<details closed><summary>banlist_project.spiders</summary>

| File                                                                                                                                       | Summary                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ---                                                                                                                                        | ---                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| [majncraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/majncraft_spider.py)                     | This code is part of a web scraping application focusing on collecting ban data from various gaming servers. The repository houses multiple spiders to crawl different game sites, with infrastructure to process and report findings.                                                                                                                                                                                                                             |
| [litebans_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/litebans_spider.py)                       | The repository, Ban-Searcher, contains a Python project for scraping various gaming websites to compile a banlist. It's structured with distinct spiders for each site and includes data processing and reporting components. The spiders extract ban data, feed into pipelines for processing, and ultimately generate a consolidated report on player bans.                                                                                                      |
| [mconline_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mconline_spider.py)                       | The Ban-Searcher repository centralizes ban data scraping for various game servers, featuring numerous specialized spiders and reporting capabilities, integrating with Google Sheets for data handling.                                                                                                                                                                                                                                                           |
| [mcbans_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mcbans_spider.py)                           | The codebase is for Ban-Searcher, which likely scans various gaming communities for bans. It features numerous spiders tailored to specific platforms (indicated by the _spider.py files), and integrates data handling via dedicated items, middlewares, and pipelines. It seems also to include reporting capabilities, possibly summarizing ban data in reports generated from templates.                                                                       |
| [banmanager_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/banmanager_spider.py)                   | This code snippet belongs to a spider within a web scraping project that aggregates Minecraft ban data, likely contributing to a larger ban monitoring or reporting system.                                                                                                                                                                                                                                                                                        |
| [banmanager_bonemeal_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/banmanager_bonemeal_spider.py) | The code snippet is part of a modular spider-based web scraping system focusing on collecting ban data from various sources, structured to enable easy addition and maintenance of specialized crawlers for different gaming communities.                                                                                                                                                                                                                          |
| [strongcraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/strongcraft_spider.py)                 | The code snippet is a component of the Ban-Searcher repository, which is a web scraping framework aimed at collecting ban data from various Minecraft servers. The architecture suggests a modular design with specialized spiders for different sources, facilitating the aggregation and reporting of player ban information.                                                                                                                                    |
| [johnymuffin_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/johnymuffin_spider.py)                 | This repository, Ban-Searcher, includes a Scrapy project for aggregating player bans from various Minecraft servers, with specialized spiders for each server and Google Sheets integration for ban data management.                                                                                                                                                                                                                                               |
| [guster_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/guster_spider.py)                           | The codebase is a web-scraping engine for compiling ban data from various gaming communities, with individual spiders tailored for different server formats, a reporting system, and integration with Google Sheets.                                                                                                                                                                                                                                               |
| [syuu_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/syuu_spider.py)                               | This repository, Ban-Searcher, is structured for web scraping, targeting various online game ban lists. It contains multiple spider scripts for different servers, middleware, and pipelines for data processing, and integrates with Google Sheets and reporting tools.                                                                                                                                                                                           |
| [cultcraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/cultcraft_spider.py)                     | This codebase represents a scraping tool designed for tracking and reporting bans across multiple Minecraft servers. It includes various spiders for different server ban systems, banlist processing logic, and report generation.                                                                                                                                                                                                                                |
| [cosmicgames_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/cosmicgames_spider.py)                 | This spider (`CosmicGamesSpider`) scrapes player ban data from Cosmic Games' API and yields translated ban items for the Ban-Searcher's architecture.                                                                                                                                                                                                                                                                                                              |
| [mundominecraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mundominecraft_spider.py)           | The code snippet likely pertains to a web scraping application focused on collecting ban information for various gaming servers, as the spiders indicate data extraction from multiple sources, and the architecture supports data reporting and user identification conversions within the gaming community.                                                                                                                                                      |
| [cubeville_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/cubeville_spider.py)                     | The code snippet is likely part of a web scraping framework, designed to gather ban data from various gaming communities. It contributes to a broader system that monitors and reports player bans, interfacing with a repository that facilitates data extraction, transformation, and subsequent reporting or analysis.                                                                                                                                          |
| [manacube_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/manacube_spider.py)                       | This repository supports a ban-search service for Minecraft servers. The code enables automated scraping of banlists from various server plugins, integrates with Google Sheets, and generates player ban reports.                                                                                                                                                                                                                                                 |
| [mcbouncer_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mcbouncer_spider.py)                     | This code snippet is part of a web scraping application within the Ban-Searcher repository, designed to automate the collection of player ban data from various gaming server sites.                                                                                                                                                                                                                                                                               |
| [google_sheets.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/google_sheets.py)                           | The code is part of a scraper tool within the Ban-Searcher repository, designed to gather ban data from various gaming communities, likely for moderation purposes.                                                                                                                                                                                                                                                                                                |
| [snapcraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/snapcraft_spider.py)                     | This repository, Ban-Searcher, contains a collection of spiders for web scraping ban data from various gaming servers, integrates a reporting system, and facilitates ban management tasks, crucial to maintaining fair play in online gaming communities.                                                                                                                                                                                                         |
| [democracycraft_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/democracycraft_spider.py)           | This repository, Ban-Searcher, likely functions as a ban tracking system for gaming communities. Its architecture includes multiple spiders for ban data retrieval across various gaming platforms (e.g., BanManager, CosmicGames), data processing components (e.g., items, pipelines), and reporting features (player_report, report). The code directs the scraping of player ban information and integrates it into a centralized reporting structure.         |
| [mcbrawl_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mcbrawl_spider.py)                         | The provided code snippet is part of a web scraping application within the Ban-Searcher repository. It's one of many spiders responsible for crawling specific game servers or platforms to aggregate banned player data, which in turn contributes to a centralized ban reporting system. This spider, like others in its directory, plays a critical role in data collection to maintain the repository's overarching goal of banlist management and monitoring. |
| [mccentral_spider.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/banlist_project/spiders/mccentral_spider.py)                     | The provided code snippet pertains to a web scraping application organized for ban tracking, specifically targeting different gaming communities to aggregate ban data.                                                                                                                                                                                                                                                                                            |

</details>

<details closed><summary>report</summary>

| File                                                                              | Summary                                                                                                                                               |
| ---                                                                               | ---                                                                                                                                                   |
| [report.py](https://github.com/Kiddooo/Ban-Searcher/blob/master/report/report.py) | The `report.py` serves as a Flask web application within the Ban-Searcher repo, providing a web interface and an API endpoint to display ban reports. |

</details>

<details closed><summary>report.templates</summary>

| File                                                                                          | Summary                                                                                                                                                                          |
| ---                                                                                           | ---                                                                                                                                                                              |
| [index.html](https://github.com/Kiddooo/Ban-Searcher/blob/master/report/templates/index.html) | The repository manages a scraping service focused on aggregating player ban data from multiple gaming servers, automating reporting and supporting data conversion and analysis. |

</details>

---

## 🚀 Getting Started

***Requirements***

Ensure you have the following dependencies installed on your system:

* **Python**: `version x.y.z`

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

### 🤖 Running Ban-Searcher

Use the following command to run Ban-Searcher:

```sh
python main.py
```

### 🧪 Tests

To execute tests, run:

```sh
pytest
```

---

## 🛠 Project Roadmap

- [X] `► INSERT-TASK-1`
- [ ] `► INSERT-TASK-2`
- [ ] `► ...`

---

## 🤝 Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Submit Pull Requests](https://github/Kiddooo/Ban-Searcher/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github/Kiddooo/Ban-Searcher/discussions)**: Share your insights, provide feedback, or ask questions.
- **[Report Issues](https://github/Kiddooo/Ban-Searcher/issues)**: Submit bugs found or log feature requests for Ban-searcher.

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

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## 👏 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

[**Return**](#-quick-links)

---
