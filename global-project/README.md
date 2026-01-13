# Global project -> Pokemon and their moves (competivive)
*By Beatriz Albiac*

## 1. Project Overview
This project goes over the design and implementation of a complete *data engineering* solution that lets users analyze the competitive scene of the multiple games that form part of the Pokémon franchise. **The objective** is to allow players, both competitive and casual, to make informed decisions about the composition of their teams and their battle strategies using structured data.

The project works in a similar way to a well organized information management system: it collects data from different sources, tidies it up, and keeps it updated automatically so it is always ready to be used. Thanks to this, users can explore the data in a reliable way, identify patterns, and make better choices through clear data visualizations, such as interactive graphs, without needing to know a whole lot about the technical specifics.

**Stated in more technical terms**, the project develops a *data pipeline* that integrates multiple datasets through an *ETL process (Extract, Transform, and Load)*. The data is stored in a *dimensionally modeled data warehouse*. The pipeline is executed automatically on a daily basis and is monitored through logs and alerts, which allow tracking what has happened and identifying whether any issues require attention. Finally, the data is made available to users through an interactive dashboard for visualization.

This system allows us to answer **critical questions** such as:
- Which combination of moves gives the best type coverage?
- Which Pokémon are the most used in each competitive category?
- Which Pokémon are the highest beneficiaries of the STAB (Same Type Attack Bonus) buff?
- Which Pokémon have the best stats?

This information is crucial to build competitive teams and to analyze the popular strategies currently being used.

This document also covers the **business factors**; mainly, it focuses on the scalability of the project, the cost of migrating it to the cloud, the opportunities for AI integration, and the concerns about privacy that may arise, showing how the solution could evolve into a system ready for production.

## 2. Datasets

In this project, two datasets are used. Both are centered around competitive data from the games, but they cover different aspects of it. They were chosen specifically because of how well related they are to one another, complementing each otherno. One of them describes the Pokémon themselves, while the other dives further into the moves used during battles. Together, they form the complete picture needed for competitive team building.

It is like having two pages of instructions in a chess box: one shows all the pieces that exist and how they move, while the other shows the strategies and plays you can make with those pieces. You need both of them to understand how the game really works.

*The datasets were found on https://www.kaggle.com/datasets/n2cholas/competitive-pokemon-dataset/, but they were extracted from https://github.com/beatrizalbiac/Ing-Datos-datasets/tree/main/global-project so as not to download them directly to the machine.*

---

### 2.1 Pokémon Dataset
**Attributes:**

- **Name**: The name of the Pokémon, written as a *String* (a sequence of characters).
- **Types**: The type or types of the Pokémon, written as a *list of Strings*. There currently exist only 18 types.
- **Abilities**: The abilities the Pokémon has, written as a *list of Strings*.
- **Tier**: The competitive tier or category the Pokémon falls under, written as a *String*. The following tiers exist: LC, PU, NU, RU, OU, UU, Uber, UUBL, RUBL, NUBL, PUBL, Limbo, AG.
  <p align="center">
    <img width="500" height="444" alt="image (4)" src="https://github.com/user-attachments/assets/53145dc2-3f31-4c62-8841-2e9583658155" />
  </p>
  
  - **PU, NU, RU, UU, OU, and Uber**: These tiers are related to one another and are separated by the usage of each Pokémon in the competitive scene. The least used Pokémon belong to the PU tier (the acronym does not have a specific meaning), and in that format only Pokémon from that tier can be used. <br>
    In the NU tier (Never Used), only Pokémon from NU and PU can be used, and they are used more frequently than those in PU. This pattern repeats for the remaining tiers. RU stands for Rarely Used, UU for Under Used, and OU for Over Used. This establishes the following hierarchy: **PU < NU < RU < UU < OU < Uber**.
  - **UUBL, RUBL, NUBL, PUBL**: These tiers work in the same way as the previous ones, but *BL* stands for *Banned List*, meaning they include Pokémon banned from each corresponding format.
  - **LC**: *Little Cup* is a format where players may only use Pokémon that have not yet evolved, are capable of evolution, and are obtainable at level 5 in-game.
  - **Limbo**: Indicates that a Pokémon’s tier has not yet been decided.
  - **AG**: *Anything Goes* is a 6v6 singles metagame with the fewest restrictions of any format.
- **HP**: *Hit Points*, a value that determines how much damage a Pokémon can endure, written as an *Integer*.
- **Attack**: Determines how much damage a Pokémon deals when using a physical move, written as an *Integer*.
- **Defense**: Determines how much damage a Pokémon resists when hit by a physical move, written as an *Integer*.
- **Special Attack**: Determines how much damage a Pokémon deals when using a special move, written as an *Integer*.
- **Special Defense**: Determines how much damage a Pokémon resists when hit by a special move, written as an *Integer*.
- **Speed**: Determines turn order in battle; generally, the Pokémon with the higher Speed attacks first. Written as an *Integer*.
- **Next Evolution(s)**: A list of Pokémon into which the current Pokémon can evolve, written as a *list of Strings*.
- **Moves**: A *list of Strings* containing the names of the moves the Pokémon can learn or use. **This is the attribute used to relate the two datasets.**


### 2.2 Moves Dataset
**Attributes:**

- **Index**: A unique identifier for each move, written as an *Integer*.
- **Name**: The name of the move, written as a *String*.
- **Type**: The type of the move, written as a *String*.
- **Category**: The move category (Physical, Special, or Status), written as a *String*.
- **Contest**: The Pokémon Contest category the move belongs to (used in contest-style modes rather than standard battles), written as a *String*.
- **PP**: *Power Points*, the number of times the move can be used before it needs to be restored, written as an *Integer*.
- **Power**: The base damage value of the move in battle, written as an *Integer* or *None* when the move does not have a fixed damage value (for example, Status moves).
- **Accuracy**: The chance of the move hitting its target, written as an *Integer* or *None* when accuracy is not defined.
- **Gen**: The generation in which the move was introduced, written as an *Integer*.

### 2.3 Dataset Relationship and Extra Mechanics

The two datasets are connected through the **Moves** attribute in the Pokémon dataset, which contains a list of move names that reference entries in the Moves dataset. This creates a many-to-many relationship that is essential for competitive analysis.<br><br>

**Additional mechanics**
- **STAB**: When a Pokémon uses a move that shares a type with it, there is an attack bonus of 50%.
- **Total stats**: The sum of a Pokémon’s stats found in the Pokémon dataset.<br><br>

For users to build competitive teams easily, the following aspects have to be taken into account:
- **Type coverage**: Each type has other types that it is strong or weak against.
- For a team to be balanced, each Pokémon needs to have complementary stats and diverse move sets.
- Each Pokémon has certain moves that work best with it; for example, a slow but bulky Pokémon benefits from high-power moves, while a fast but fragile one benefits from accurate moves.
- A Pokémon with mediocre stats but unique moves might still be worth considering. The same can be said for the opposite case.


## 3. Architecture Overview
This project implements a data architecture that transforms raw Pokémon data into an analytic database. The system is built around four main components that work together to move the data from the CSV files (the datasets) they come from to the data that users see and use.<br><br>

**Main Components:**

<p align="center">
    <img width="661" height="61" alt="WORKFLOW BASE ID drawio" src="https://github.com/user-attachments/assets/66fc5287-b2b7-4c79-b1a5-f7a04b633953" />
</p>

1. **The source**: These are the base CSV files found in the other GitHub repository specifically created to store them. They contain the raw data, which is explored by the Python notebook included in the project. They act as the single source of truth.
2. **ETL**: This is the processing system that manages the transformation of the data. It will be explained further later in the document.
3. **Data warehouse**: This is a SQLite database with a dimensional model. It stores only cleaned and structured data.
4. **Data consumption**: This layer allows interactive exploration of the data. It includes analytics and visualizations oriented toward the user.


## 4. Data Lifecycle Management
This project covers all phases of the data lifecycle, as shown in the previous diagram. Following what was covered in class, the data lifecycle follows this linear path: **Generation → Ingestion → Storage → Processing → Serving/Analysis**

### 4.1 Generation
As previously stated, the data is downloaded from the web, so it is not generated by the system itself. These CSV files are scraped from official web pages such as:
- Smogon: https://www.smogon.com/dex/sm/pokemon/
- Bulbapedia: https://bulbapedia.bulbagarden.net/wiki/List_of_moves

### 4.2 Ingestion
A batch ingestion approach is used, where data is collected in large groups (batches) over time and then moved, processed, and loaded into the system at scheduled intervals rather than in real time. The decision to use this approach relies on the fact that updates to the database are not frequent; updates are only required when a new game or generation is released or when changes occur in the competitive scene, which does not happen on a daily basis. The volume of data is also perfectly manageable, so this is not an issue. Additionally, batch ingestion is easier to implement than streaming systems.

### 4.3 Storage
There are three different iterations of data being stored: the raw CSV files, the cleaned CSV files, and the data processed into the data warehouse.<br><br>
Storing the raw data allows the data to be reprocessed without having to download it again, and the same applies once the data has been transformed.

### 4.4 Processing
For this project, an ETL process was chosen instead of an ELT process. The main reason is that ETL validates data quality before it enters the data warehouse. It also reduces computational costs and keeps raw data separate for safety and traceability.

### 4.5 Serving
Data serving is done through interactive graphs and Looker Studio.

## 5. ETL Design
The pipeline, as explained before, transforms raw data into data ready to be loaded into the data warehouse, following this pattern: **Extract → Transform → Load**. In this case, there are some additional steps, but the main flow remains the same.

**General flow:**
<p align="center">
    <img width="1238" height="221" alt="WORKFLOW BASE ID drawio (1)" src="https://github.com/user-attachments/assets/56553080-66b3-4359-9c73-d6de31a4c087" />
</p>

1. **Extract**: The data is downloaded from GitHub and saved into a raw folder.
2. **Transform**:
    1. The moves column is parsed, converting the data from a list of strings into a Python list.
    2. Move names are standardized.
    3. Total stats are calculated from the individual stats in the CSV files.
    4. Required type conversions are applied.
    5. Null values are cleaned when necessary; in this case, only when the Contest field has a `???` value.
    6. The cleaned CSV files are stored in a processed folder.
3. **Load**: Specific scripts are used to transform the cleaned CSV files into the structure required by the data warehouse, which is explained in the next section of the document. The order in which these scripts are executed is **crucial**, as some tables depend directly on others through foreign keys. The execution order is:
    1. `dim_generations`
    2. `dim_types`
    3. `dim_moves`
    4. `dim_abilities`
    5. `dim_pokemon`
    6. `bridge_pokemon_types`
    7. `bridge_pokemon_abilities`
    8. `fact_pokemon_moves`
    9. Updates to `evolves_from_id` in `dim_pokemon`

This process ensures that duplicate data is not inserted and that the pipeline can run smoothly.

## 6. Data Warehouse Model
The data warehouse uses a **Star Schema**, which is formed by a central table containing quantitative metrics (facts), surrounded by descriptive tables (dimensions) that provide context to the fact table, such as who, what, when, and where.

<p align="center">
    <img width="1109" height="1103" alt="dimensional model" src="https://github.com/user-attachments/assets/506009c1-ab85-4de3-b332-bc8df4c16bfe" />
</p>

_Done using https://dbdiagram.io/_

The schema is composed of five dimension tables, two bridge tables used to represent many-to-many relationships, and one fact table.

***All specifications defining the contents of each table are described in the `schema.sql` file.***

The model is **partially denormalized** in order to optimize query performance:
- Combat statistics such as HP, Attack, and Defense are stored directly in the `dim_pokemon` table instead of being separated into another table.
- The `total_stats` attribute could be calculated through a query, but storing it directly simplifies analysis.

The design prioritizes query performance, even if this introduces a small amount of redundancy in the data warehouse.

This makes the data warehouse an **OLAP (Online Analytical Processing)** system because ...............................

All dimensions follow a Slowly Changing Dimension (SCD) strategy between **Type 0 and Type 1**. Most of the data is not expected to change, but since game updates or competitive tier adjustments may occur, some attributes need to be updated. In these cases, the chosen approach is to overwrite existing values, which corresponds to an SCD Type 1 strategy.

## 7. Orchestration Strategy
## 8. Monitorization (logging and alerting)
## 10. Data Visualization (Looker Studio)
This is just some query examples:
https://lookerstudio.google.com/reporting/2e0886e6-69a9-4980-82a0-855841e56488
## 11. Data Insights
## 12. Scalability Analysis
## 13. Cloud Cost Estimation
## 14. AI Contribution
## 15. Privacy Considerations
## 16. How to Run the Project
