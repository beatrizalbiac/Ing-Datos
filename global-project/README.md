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

This makes the data warehouse an **OLAP (Online Analytical Processing)** system because it is designed for running analytical queries and reporting, not for handling frequent data updates like a transactional database would.

All dimensions follow either a **Slowly Changing Dimension (SCD) strategy Type 0** or a **SCD Type 1**. Most of the data is not expected to change, but since game updates or competitive tier adjustments may occur, some attributes need to be updated. In these cases, the chosen approach is to overwrite existing values, which corresponds to an SCD Type 1 strategy.

## 7. Orchestration Strategy
The pipeline orchestration is handled by a simple Python script called `main.py`. It runs the four ETL stages one after another: creating the database, extracting the data, transforming it, and loading it into the warehouse. If any stage fails, the whole pipeline stops immediately thanks to the `check=True` flag in `subprocess.run()`.

Everything is logged to `logs/pipeline.log`, including timestamps and how long each stage took. This makes it easy to understand what happened if something goes wrong.

This straightforward approach was chosen instead of using tools like Apache Airflow or cloud orchestrators because the pipeline is simple enough that it does not require advanced features such as parallel tasks or complex dependencies. The main advantage is that there is nothing extra to install or manage; it is just Python code that is easy to debug and run.

### Daily Scheduling
In a production environment, this pipeline should run automatically once a day. Here's how you'd set that up:

**On Windows (using Task Scheduler):**
Create a scheduled task that runs `python main.py` at the desired time each day.

**On Linux/Mac (using cron):**
```bash
# runs every day at 2 AM
0 2 * * * cd /path/to/project && python main.py >> logs/cron.log 2>&1
```

**Why once a day?** The competitive Pokémon meta does not change very frequently, so running the pipeline more often would not provide significant benefits. Daily batch processing is efficient and aligns well with the batch ingestion approach used throughout the project. It could even be less frequent (for example, once every three days) and still be fine.

Since this is currently a local project, the pipeline is executed manually using `python main.py` when needed. However, the configuration above shows how it could be easily automated if required.

## 8. Monitorization (logging and alerting)
The pipeline uses Python’s built in `logging` module to keep track of what happens during execution. Logging is used as the main monitoring mechanism, since it allows understanding both whether the pipeline ran correctly and where a problem occurred if something fails.

Two different log files are generated for clarity, one that manages the whole pipeline flow, while the other manages the `load.py` flow regarding every script that conforms it. `pipeline.log` records when each ETL stage starts and finishes, how long it took, and any errors. `load.log` records how many rows were inserted into the warehouse and how long the loading took.

Each log entry includes a timestamp, a severity level such as INFO or ERROR, and a short message describing what happened. This structure makes the logs easy to read and useful both for quick checks and for more detailed analysis when something goes wrong.

### Alerting (Not Implemented)

For this project, no automatic alerting system is implemented, as the pipeline is executed locally. In this context, manually checking the logs is sufficient.

In a real production environment, alerting would be essential. For example, the system could send an email or a *Slack* message if the pipeline fails, including information about which stage failed and the associated error message. Alerts could also be triggered if the pipeline takes much longer than usual or if the number of rows loaded is very different from previous executions.

Alerting is important because, without it, a failed pipeline might go unnoticed and result in outdated or incomplete data. Automated alerts allow problems to be detected early and fixed before they affect users. While this is not required for the current scope of the project, it would be a necessary addition in any production level deployment.

## 9. Data Visualization (Looker Studio), and data insights
This is just some query examples:
https://lookerstudio.google.com/reporting/2e0886e6-69a9-4980-82a0-855841e56488

### Dashboard Contents

The dashboard includes five visualizations designed to answer some of the key questions related to the competitive Pokémon scene:

1. **Pokémon per Tier**: Shows the distribution of Pokémon across competitive tiers, highlighting which tiers contain the greatest variety.
2. **Top 10 Highest Stats**: Displays the Pokémon with the highest total base stats, providing an overview of the strongest entries in terms of raw attributes.
3. **Moves per Generation**: Illustrates how many moves were introduced in each generation, allowing comparison of design complexity across generations.
4. **Best Stats per Tier**: Compares average base stats across competitive tiers, helping validate the relationship between Pokémon strength and tier placement.
5. **Best Stats per Type**: Shows which Pokémon types have the highest aggregate stats, enabling comparisons between different type groups.

Users can filter the visualizations by generation, type, or tier to explore specific subsets of the data. All charts update dynamically based on the selected filters.

Overall, the dashboard allows users to analyze the competitive meta without requiring SQL knowledge, making it easier to identify trends and compare Pokémon across multiple criteria.<br>
*There are way more graphs that could have been done, these are just a snippet to explain how it would work, and what the users would see*

### Data Insights
**Tier System Validation:**  
The data confirms that Pokémon tiers are closely related to their stats. Pokémon in the AG tier have an average of around 730 total base stats, while Pokémon in lower tiers have much lower averages. Lower tiers such as PU and LC also contain many more Pokémon than the top tiers, which gives players more variety when building teams.

**Power Creep:**  
Mega Evolutions and Primal forms dominate the list of Pokémon with the highest total stats, all exceeding 700 points. Even so, Generation I introduced the highest number of moves, with around 170. Newer generations add fewer moves, suggesting that the game design has shifted away from adding new moves and toward improving or rebalancing existing mechanics.

**Type Dominance:**  
Water, Flying, and Psychic types have the highest combined stats overall, which helps explain why they appear so often in competitive play. In contrast, Rock and Bug types tend to have lower overall stats and are less dominant.

**Data Quality:**  
The main data quality issue encountered was inconsistent formatting of apostrophes in move names, such as `"Forest-s Curse"` versus `"Forest's Curse"`. Aside from this, the dataset was generally clean, with very few missing values. Missing Power or Accuracy values only occurred for status moves, which is expected behavior.

**Value for Players:**  
The data warehouse allows competitive players to quickly answer questions like *“Which are the best Water-type Pokémon in OU?”* or *“Which moves provide STAB for my team?”* without having to search through multiple websites. This significantly speeds up team-building analysis and decision-making.

## 10. Scalability Analysis
To evaluate how the system would behave if the amount of data increased, several growth scenarios were considered by multiplying the number of rows in the datasets. The goal is to understand both where the current design starts to struggle and how those limitations could be addressed.

- **x10**: With ten times more data, the current solution would continue to work without major issues. The pipeline would take slightly longer to run, but performance would remain stable. In this case, the main action needed would be minor optimizations, such as grouping inserts into batches and avoiding unnecessary recalculations during the transformation step.

- **x100**: At this scale, the increase in data becomes more noticeable. Transformation and loading steps would require more time, and analytical queries could start to slow down. To address this, performance improvements would focus on efficiency, such as using bulk operations consistently, adding indexes to frequently queried columns, and optimizing joins in the data warehouse.

- **x1000**: When the data grows to this level, the limitations of SQLite become clear. Both data loading and query execution would slow down significantly, and concurrent access would not be well supported. The most appropriate solution at this point would be to migrate the data warehouse to a more robust relational database such as PostgreSQL, keeping the same star schema but benefiting from better performance and scalability.

- **x10⁶**: With very large volumes of data, the current architecture would no longer be suitable. Processing everything on a single machine would not be realistic. To handle this scenario, the system would need to move to a cloud based setup, using object storage for files, scalable compute resources for ETL execution, and a managed analytical database capable of handling large scale queries.

Overall, this analysis shows that the project not only works for the current dataset size, but also defines clear steps to address scalability issues as data grows, making future evolution of the system easier to plan and justify.

## 11. Cloud Cost Estimation

To estimate the cost of migrating this project to the cloud, AWS was selected as the reference cloud provider. The estimation was performed using the AWS Pricing Calculator and focuses on the main components required by the system: object storage for raw and processed data using Amazon S3, and a managed relational database for analytical queries using Amazon RDS with PostgreSQL.

<p align="center">
    <img width="3550" height="945" alt="image" src="https://github.com/user-attachments/assets/6fc84db4-89e3-49c8-b103-4a00a049d0eb" />
</p>
The picture shows the estimated monthly cost for a small-scale deployment, assuming 10 GB of storage in S3 and a small PostgreSQL RDS instance. Under these conditions, the estimated monthly cost is approximately 20$, resulting in a yearly cost of around 250$. (These data was just an estimation and in no way is 100% accurate)

Based on this baseline, different data growth scenarios can be considered:

- **x10**: With ten times more data, storage requirements increase slightly, while compute and database resources remain mostly unchanged. The estimated monthly cost would increase marginally and remain well below 30$.

- **x100**: At this scale, storage costs become more noticeable, and the database may require additional resources. Even so, the total monthly cost would still remain relatively low, likely within the range of a few tens of dollars.

- **x1000**: With a significantly larger volume of data, both storage and database resources would need to scale. This would require a larger database instance and increased storage capacity, pushing monthly costs into the range of several tens to low hundreds of dollars.

- **x10⁶**: At very large scale, costs increase substantially. Scalable storage, more powerful database instances, and potentially additional compute resources would be required. In this scenario, monthly costs could reach several hundreds of dollars, depending on usage patterns and optimization decisions.

These values are not intended to represent exact production costs, but rather to provide an order-of-magnitude estimation. This analysis shows that cloud migration is affordable at small and medium scales, while cost becomes a key factor as data volume grows, reinforcing the importance of scalability planning.


## 12. AI Contribution
Artificial Intelligence could support this project mainly at the analysis and data quality stages. For example, AI models could be used to detect unusual changes in Pokémon usage or move popularity over time, helping identify shifts in the competitive meta. AI could also assist in validating incoming data by automatically flagging inconsistencies or missing values during the transformation process, reducing the need for manual checks and improving overall data reliability.

## 13. Privacy Considerations
This project uses only publicly available data related to Pokémon game mechanics and competitive usage. No personal or sensitive user data is collected, stored, or processed.

As a result, privacy risks are minimal and no specific privacy protection measures are required. If user data were to be introduced in the future, appropriate privacy and data protection mechanisms would need to be considered. But introducing user data would make no sense.

## 14. What I would have done differently if I were to start again
I would choose to save the data warehouse into PostgreSQL instead of SQLite, as trying to make the dashboard in Looker studio, and calculate the could costs in AWS was a pain, and I would end up having to migrate it anyways.
