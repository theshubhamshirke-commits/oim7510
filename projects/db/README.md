# 1. The Scenario

I chose Scenario A: BabsonAI Labs.

BabsonAI Labs is a startup founded by Babson students that builds
AI tools for small businesses. It has about 25 people and currently
tracks its work in spreadsheets and chat threads.

The database will organize information about employees, projects,
project memberships, tasks, and expenses. It will help the founders
understand who works on each project, how project spending compares
with budgets, and which employees are overloaded.


# 2. The ERD

```mermaid
erDiagram
    PEOPLE |o..o{ PEOPLE : manages
    PEOPLE ||--o{ PROJECT_MEMBERSHIPS : has
    PROJECTS ||--|{ PROJECT_MEMBERSHIPS : includes
    PROJECTS ||..o{ TASKS : contains
    PEOPLE |o..o{ TASKS : receives
    PROJECTS ||..o{ EXPENSES : incurs

    PEOPLE {
        int person_id PK
        varchar first_name
        varchar last_name
        varchar work_email UK
        varchar title
        date start_date
        int manager_id FK "NULL when there is no manager"
    }

    PROJECTS {
        int project_id PK
        varchar project_name
        varchar client_name "NULL for internal projects"
        varchar category
        decimal budget
        date start_date
        varchar status
    }

    PROJECT_MEMBERSHIPS {
        int person_id PK, FK
        int project_id PK, FK
        varchar project_role
        decimal weekly_hours
        date joined_date
    }

    TASKS {
        int task_id PK
        int project_id FK
        varchar description
        date created_date
        int assigned_person_id FK "NULL when unassigned"
        date assigned_date "NULL when unassigned"
        date due_date
        date completed_date "NULL until completed"
    }

    EXPENSES {
        int expense_id PK
        int project_id FK
        date expense_date
        decimal amount
        varchar category
        varchar note
    }
```


# 3. What One Row Means

- **people:** One row represents one employee at BabsonAI Labs,
  including their details and the manager they report to, if any.

- **projects:** One row represents one project tracked by BabsonAI
  Labs, including its budget, start date, category, and status.

- **project_memberships:** One row represents one employee's
  membership in one project, including their role, weekly hours,
  and the date they joined that project.

- **tasks:** One row represents one task belonging to one project,
  including its dates and the employee assigned to it, if any.

- **expenses:** One row represents one expense incurred for one
  project, including its date, amount, category, and note.

# 4. Design Choices