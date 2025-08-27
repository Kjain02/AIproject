# Define weight structure for the ESG scorecard with normalized category weights
weights = {
    "environmental": {
        "weight": 0.4,
        "categories": {
            "environmental_impact": 0.25,
            "carbon_emissions_management": 0.25,
            "resource_usage_efficiency": 0.25,
            "waste_management_pollution_control": 0.125,
            "climate_change_adaptation_risk": 0.125
        }
    },
    "social": {
        "weight": 0.3,
        "categories": {
            "employee_relations_satisfaction": 0.2667,
            "diversity_inclusion": 0.2667,
            "health_safety_practices": 0.2333,
            "labor_standards_human_rights": 0.1333,
            "community_engagement_social_responsibility": 0.1
        }
    },
    "governance": {
        "weight": 0.3,
        "categories": {
            "board_structure_independence": 0.2667,
            "executive_compensation": 0.1667,
            "shareholder_rights_transparency": 0.1667,
            "audit_risk_management": 0.1333,
            "ethical_business_practices": 0.1,
            "succession_planning_leadership_stability": 0.1,
            "stakeholder_engagement": 0.0667
        }
    }
}

# Helper function to calculate weighted score for each category
def calculate_weighted_score(category_scores, category_weights):
    total_score = 0
    total_weight = 0
    for category, weight in category_weights.items():
        score = category_scores.get(category)
        if score is not None:
            total_score += score * weight
            total_weight += weight
        else:
            # Handle missing scores by adjusting the total weight
            total_weight += weight
            print(f"Warning: Missing score for {category}. Using zero in calculation.")
    if total_weight == 0:
        return 0
    # Since total_weight is normalized to 1, weighted_average_score = total_score
    weighted_average_score = total_score / total_weight
    # Adjust the score to be in range 1 to 4.9
    if weighted_average_score < 1:
        weighted_average_score = 1
    elif weighted_average_score > 4.9:
        weighted_average_score = 4.9
    return weighted_average_score / 20  # Divide by 20 to scale from 0-100 to 0-5

# Main function to calculate the ESG scorecard
def calculate_esg_scorecard(esg_scores):
    # Initialize scores
    environmental_score = 0
    social_score = 0
    governance_score = 0

    # Extract scores from the input data
    environmental_scores = esg_scores.get("environment_score", {})
    social_scores = esg_scores.get("social_score", {})
    governance_scores = esg_scores.get("governance_score", {})

    # Calculate environmental score
    environmental_weighted_score = calculate_weighted_score(
        environmental_scores,
        weights["environmental"]["categories"]
    )
    environmental_score = environmental_weighted_score * weights["environmental"]["weight"]

    # Calculate social score
    social_weighted_score = calculate_weighted_score(
        social_scores,
        weights["social"]["categories"]
    )
    social_score = social_weighted_score * weights["social"]["weight"]

    # Calculate governance score
    governance_weighted_score = calculate_weighted_score(
        governance_scores,
        weights["governance"]["categories"]
    )
    governance_score = governance_weighted_score * weights["governance"]["weight"]

    # Calculate total ESG score
    total_esg_score = environmental_score + social_score + governance_score

    # Return individual scores and total score
    return {
        "environmental_score": round(environmental_weighted_score, 2),
        "social_score": round(social_weighted_score, 2),
        "governance_score": round(governance_weighted_score, 2),
        "total_esg_score": round(total_esg_score, 2)
    }
