# Global project -> Pokemon and their moves (competivive)
*By Beatriz Albiac*

## 1. Project Overview
This project goes over the design and implementation of a complete *data engineering* solution that lets users analyze the competitive scene of the multiple games that form part of the Pokémon franchise. **The objective** is to allow players, both competitive and casual, to make informed decisions about the composition of their teams and their battle strategies using structured data.

The project works in a similar way to a well organized information management system: it collects data from different sources, tidies it up, and keeps it updated automatically so it is always ready to be used. Thanks to this, users can explore the data in a reliable way, identify patterns, and make better choices through clear data visualizations, such as interactive graphs, without needing to know a whole lot about the technical specifics.

**Stated in more technical terms**, the project develops a *data pipeline* that integrates multiple datasets through an *ETL process (Extract, Transform, and Load)*. The data is stored in a *dimensionally modeled data warehouse*. The pipeline is executed automatically on a daily basis and is monitored through logs and alerts, which allow tracking what has happened and identifying whether any issues require attention. Finally, the data is made available to users through an interactive dashboard for visualization.

This system allows us to answer **critical questions** such as:
- Which combination of moves gives the best type coverage?
- Which Pokémon are the most used in each competitive category?
- Which Pokémon are the highest beneficiaries of the STAB buff?
- Which Pokémon have the best stats?

This information is crucial to build competitive teams and to analyze the popular strategies currently being used.

This document also goes over the **business factors**; mainly, it focuses on the scalability of the project, the cost of migrating it to the cloud, the opportunities for AI integration, and the concerns about privacy that may arise, showing how the solution could evolve into a system ready for production.

## 2. Datasets
## 3. Architecture Overview
## 4. Data Lifecycle Management
## 5. ETL Design
## 6. Data Warehouse Model

<img width="1109" height="1103" alt="dimensional model" src="https://github.com/user-attachments/assets/506009c1-ab85-4de3-b332-bc8df4c16bfe" />
done in https://dbdiagram.io/d

## 7. Orchestration Strategy
## 8. Monitorization (logging and alerting)
## 10. Data Visualization (Looker Studio)
## 11. Data Insights
## 12. Scalability Analysis
## 13. Cloud Cost Estimation
## 14. AI Contribution
## 15. Privacy Considerations
## 16. How to Run the Project
