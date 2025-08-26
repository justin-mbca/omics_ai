```mermaid
flowchart TD
    A[User] --> B[Streamlit UI]
    B --> C[Data Loader]
    C --> D[Analysis & ML Modules]
    D --> E[Visualization Engine]
    E --> B
    D --> F[Export/Reporting]
    F --> B
    G[Omics Data (CSV/TSV)] --> C
    H[Example Data] --> B
```

```plantuml
@startuml
actor User
User -> UI : Upload omics data
UI -> DataLoader : Load/validate data
DataLoader -> Analysis : Run QC, PCA, clustering, etc.
Analysis -> Visualization : Generate plots
Visualization -> UI : Show results
UI -> Export : Download CSV/plots
@enduml
```

---

**Above:**
- **Mermaid Diagram:** Shows the modular architecture and data flow between user, UI, backend modules, and data sources.
- **PlantUML Diagram:** Illustrates the user journey and main system interactions.

> For more diagrams, see the `/docs` folder (planned).
