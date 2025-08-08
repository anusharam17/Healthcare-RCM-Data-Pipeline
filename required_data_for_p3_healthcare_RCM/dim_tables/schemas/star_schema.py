from graphviz import Digraph

# Set output directory and filename
output_path = '/Users/apple/Desktop/Healthcare/required_data_for_p3_healthcare_RCM/dim_tables/schemas/star_schema_diagram'

# Create a directed graph
dot = Digraph(comment='Healthcare Star Schema', format='png')
dot.attr(rankdir='LR', fontsize='10')

# Dimension Tables with correct number of columns
dimensions = {
    "dim_patient": [
        "PatientKey (PK)", "PatientID", "FirstName", "LastName", "DOB", "Gender", "Phone", "Email",
        "Address", "Age", "InsertedDate"
    ],
    "dim_date": [
        "DateKey (PK)", "FullDate", "Day", "Month", "Year", "Quarter", "Week", "Weekday"
    ],
    "dim_provider": [
        "ProviderKey (PK)", "ProviderID", "FirstName", "LastName", "Specialty", "Phone",
        "Email", "InsertedDate"
    ],
    "dim_procedure": [
        "ProcedureKey (PK)", "ProcedureCode", "ProcedureDescription"
    ],
    "dim_encounter": [
        "EncounterKey (PK)", "EncounterID", "PatientKey (FK)", "ProviderKey (FK)", "ProcedureKey (FK)",
        "EncounterDate", "EncounterType", "DepartmentID", "InsertedDate", "ModifiedDate", "HospitalName"
    ]
}

# Fact Tables with correct number of columns
facts = {
    "fact_transactions": [
        "TransactionKey (PK)", "PatientKey (FK)", "ProviderKey (FK)", "ProcedureKey (FK)", "DateKey (FK)",
        "EncounterKey (FK)", "Amount", "Status", "Mode", "TransactionType", "TransactionDate", "ClaimKey (FK)",
        "PaymentStatus", "InsurancePaid", "PatientPaid", "CoPay", "Deductible", "Discount", "Tax", "TotalAmount",
        "InsertedDate", "ModifiedDate", "TransactionCode", "TransactionDescription", "Currency", "PaymentMethod"
    ],
    "fact_claims": [
        "ClaimKey (PK)", "PatientKey (FK)", "ProviderKey (FK)", "ProcedureKey (FK)", "DateKey (FK)",
        "EncounterKey (FK)", "ClaimAmount", "InsurancePaid", "PatientPaid", "ClaimStatus", "ClaimType",
        "SubmissionDate", "ApprovalDate", "RejectionDate", "ClaimCode", "DiagnosisCode", "HospitalName",
        "InsertedDate"
    ]
}

# Helper function to build HTML-like table label
def make_html_table(title, columns):
    header = f"<TR><TD COLSPAN='1'><B>{title}</B></TD></TR>"
    rows = ''.join(f"<TR><TD>{col}</TD></TR>" for col in columns)
    return f"<<TABLE BORDER='1' CELLBORDER='1' CELLSPACING='0'>{header}{rows}</TABLE>>"

# Add dimension nodes
for dim_name, columns in dimensions.items():
    dot.node(dim_name, label=make_html_table(dim_name, columns), shape='plaintext', fontsize='10')

# Add fact nodes
for fact_name, columns in facts.items():
    dot.node(fact_name, label=make_html_table(fact_name, columns), shape='plaintext', color='lightblue', fontsize='10')

# Define relationships (edges) from fact tables to dimension tables
relations = [
    ("fact_transactions", "dim_patient"),
    ("fact_transactions", "dim_provider"),
    ("fact_transactions", "dim_procedure"),
    ("fact_transactions", "dim_date"),
    ("fact_transactions", "dim_encounter"),

    ("fact_claims", "dim_patient"),
    ("fact_claims", "dim_provider"),
    ("fact_claims", "dim_procedure"),
    ("fact_claims", "dim_date"),
    ("fact_claims", "dim_encounter")
]

for src, tgt in relations:
    dot.edge(src, tgt)

# Save and render the diagram as PNG
dot.render(output_path, view=True)
print(f"Diagram saved to {output_path}.png")
