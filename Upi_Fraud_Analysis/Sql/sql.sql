SELECT
    COUNT(*) AS Total_Transactions,
    COUNT(DISTINCT UserID) AS Unique_Users,
    COUNT(DISTINCT BankName) AS Total_Banks,
    COUNT(DISTINCT MerchantCategory) AS Merchant_Categories,
    ROUND(SUM(Amount), 2) AS Total_Transaction_Value,
    ROUND(AVG(Amount), 2) AS Average_Transaction_Amount
FROM transactions;

SELECT
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    COUNT(*) - SUM(FraudFlag) AS Legitimate_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate_Percentage
FROM transactions;


SELECT
    RiskLevel,
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate
FROM transactions
GROUP BY RiskLevel
ORDER BY Fraud_Rate DESC;


SELECT
    RiskScore,
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate
FROM transactions
GROUP BY RiskScore
ORDER BY RiskScore;

SELECT
    UnusualLocation,
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate
FROM transactions
GROUP BY UnusualLocation
ORDER BY Fraud_Rate DESC;


SELECT
    UnusualAmount,
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate,
    ROUND(AVG(Amount), 2) AS Average_Amount
FROM transactions
GROUP BY UnusualAmount
ORDER BY Fraud_Rate DESC;


SELECT
    NewDevice,
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate
FROM transactions
GROUP BY NewDevice
ORDER BY Fraud_Rate DESC;


SELECT
    FailedAttemptCategory,
    COUNT(*) AS Total_Transactions,
    SUM(FraudFlag) AS Fraud_Transactions,
    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate
FROM transactions
GROUP BY FailedAttemptCategory
ORDER BY Fraud_Rate DESC;


SELECT
    NewDevice,
    UnusualLocation,
    UnusualAmount,

    COUNT(*) AS Total_Transactions,

    SUM(FraudFlag) AS Fraud_Transactions,

    ROUND(
        SUM(FraudFlag) * 100.0 / COUNT(*),
        2
    ) AS Fraud_Rate

FROM transactions

GROUP BY
    NewDevice,
    UnusualLocation,
    UnusualAmount

ORDER BY
    Fraud_Rate DESC;