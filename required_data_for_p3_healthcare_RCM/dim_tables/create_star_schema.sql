USE healthcare_star;

-- ================================
-- ✅ Referential Integrity Checks
-- ================================

-- 1. Check orphaned PatientID in fact_transactions
SELECT 'Orphaned PatientID in fact_transactions' AS CheckType, ft.*
FROM fact_transactions ft
LEFT JOIN dim_patient dp ON ft.PatientID = dp.PatientID
WHERE dp.PatientID IS NULL;

-- 2. Check orphaned ProviderID in fact_transactions
SELECT 'Orphaned ProviderID in fact_transactions' AS CheckType, ft.*
FROM fact_transactions ft
LEFT JOIN dim_provider dpr ON ft.ProviderID = dpr.ProviderID
WHERE dpr.ProviderID IS NULL;

-- 3. Check orphaned ProcedureID in fact_transactions
SELECT 'Orphaned ProcedureID in fact_transactions' AS CheckType, ft.*
FROM fact_transactions ft
LEFT JOIN dim_procedure dproc ON ft.ProcedureID = dproc.ProcedureID
WHERE dproc.ProcedureID IS NULL;

-- 4. Check orphaned DateID in fact_transactions
SELECT 'Orphaned DateID in fact_transactions' AS CheckType, ft.*
FROM fact_transactions ft
LEFT JOIN dim_date dd ON ft.DateID = dd.DateID
WHERE dd.DateID IS NULL;

-- 5. Check orphaned TransactionID in fact_claims
SELECT 'Orphaned TransactionID in fact_claims' AS CheckType, fc.*
FROM fact_claims fc
LEFT JOIN fact_transactions ft ON fc.TransactionID = ft.TransactionID
WHERE ft.TransactionID IS NULL;

-- ================================
-- ✅ Business Rule Validations
-- ================================

-- 6. Transactions with Amount <= 0
SELECT 
  'Invalid Amount in fact_transactions' AS CheckType, 
  TransactionID, 
  PatientID, 
  ProviderID, 
  ProcedureID, 
  DateID, 
  Amount, 
  PaymentStatus
FROM fact_transactions
WHERE Amount <= 0;

-- 7. Claims with ClaimAmount <= 0
SELECT 
  'Invalid ClaimAmount in fact_claims' AS CheckType, 
  ClaimID, 
  TransactionID, 
  ClaimAmount, 
  SubmittedDate, 
  ApprovedDate
FROM fact_claims
WHERE ClaimAmount <= 0;

-- 8. Claim SubmittedDate after ApprovedDate
SELECT 
  'SubmittedDate > ApprovedDate in fact_claims' AS CheckType, 
  ClaimID, 
  TransactionID, 
  ClaimAmount, 
  SubmittedDate, 
  ApprovedDate
FROM fact_claims
WHERE ApprovedDate IS NOT NULL AND SubmittedDate > ApprovedDate;

-- ================================
-- ✅ Duplicate Key Checks in Dimensions
-- ================================

-- 9. Duplicate PatientID in dim_patient
SELECT 'Duplicate PatientID in dim_patient' AS CheckType, PatientID, COUNT(*) AS cnt
FROM dim_patient
GROUP BY PatientID
HAVING cnt > 1;

-- 10. Duplicate ProviderID in dim_provider
SELECT 'Duplicate ProviderID in dim_provider' AS CheckType, ProviderID, COUNT(*) AS cnt
FROM dim_provider
GROUP BY ProviderID
HAVING cnt > 1;

-- 11. Duplicate ProcedureID in dim_procedure
SELECT 'Duplicate ProcedureID in dim_procedure' AS CheckType, ProcedureID, COUNT(*) AS cnt
FROM dim_procedure
GROUP BY ProcedureID
HAVING cnt > 1;

-- 12. Duplicate DateID in dim_date
SELECT 'Duplicate DateID in dim_date' AS CheckType, DateID, COUNT(*) AS cnt
FROM dim_date
GROUP BY DateID
HAVING cnt > 1;
