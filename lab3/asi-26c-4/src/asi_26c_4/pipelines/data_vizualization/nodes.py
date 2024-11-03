"""
This is a boilerplate pipeline 'data_vizualization'
generated using Kedro 0.19.9
"""
import matplotlib.pyplot as plt
import seaborn as sns


def satisfaction_score_distribution(df, save_path="data/08_reporting/satisfaction_score_distribution.png"):
    plt.figure(figsize=(8, 6))
    sns.histplot(df['Employee_Satisfaction_Score'], kde=True)
    plt.title("Distribution of Employee Satisfaction Score")
    plt.xlabel("Employee Satisfaction Score")
    plt.ylabel("Frequency")
    plt.savefig(save_path)
    plt.close()
    return df


def corelation_matrix_vizualization(df, save_path="data/08_reporting/corelation_matrix_vizualization.png"):
    correlation_matrix = df.corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("Correlation Matrix")
    plt.savefig(save_path)
    plt.close()
    return df