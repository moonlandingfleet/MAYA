package com.mayaboss.android.util

import com.mayaboss.android.model.Proposal
import kotlin.math.max

object ProposalScoringUtil {
    
    /**
     * Calculate ROI (Return on Investment) for a proposal
     * ROI = (Expected Revenue - Cost) / Cost
     */
    fun calculateROI(proposal: Proposal): Double {
        if (proposal.cost_eth <= 0) return 0.0
        
        // Convert BTC revenue to ETH equivalent (simplified conversion)
        val btcToEthRate = 15.0 // Simplified rate, in real app this would come from an API
        val expectedRevenueEth = proposal.expected_monthly_revenue_btc * btcToEthRate
        
        return (expectedRevenueEth - proposal.cost_eth) / proposal.cost_eth
    }
    
    /**
     * Calculate a comprehensive score for a proposal based on multiple factors
     */
    fun calculateProposalScore(proposal: Proposal): Double {
        // Base ROI score (30% weight)
        val roi = calculateROI(proposal)
        val roiScore = normalizeROI(roi) * 0.3
        
        // Revenue stability score (20% weight)
        val revenueStabilityScore = calculateRevenueStabilityScore(proposal) * 0.2
        
        // Cost efficiency score (15% weight)
        val costEfficiencyScore = calculateCostEfficiencyScore(proposal) * 0.15
        
        // Strategic impact score (20% weight)
        val strategicImpactScore = calculateStrategicImpactScore(proposal) * 0.2
        
        // Collaboration value score (10% weight)
        val collaborationScore = calculateCollaborationScore(proposal) * 0.1
        
        // Risk score (5% weight)
        val riskScore = calculateRiskScore(proposal) * 0.05
        
        return max(0.0, roiScore + revenueStabilityScore + costEfficiencyScore + strategicImpactScore + collaborationScore - riskScore)
    }
    
    /**
     * Normalize ROI to a 0-1 scale
     */
    private fun normalizeROI(roi: Double): Double {
        // Assume maximum reasonable ROI is 1000% (10.0)
        val maxROI = 10.0
        return when {
            roi <= 0 -> 0.0
            roi >= maxROI -> 1.0
            else -> roi / maxROI
        }
    }
    
    /**
     * Calculate revenue stability score based on expected revenue
     */
    private fun calculateRevenueStabilityScore(proposal: Proposal): Double {
        // Higher expected revenue generally indicates more stable income
        // Assuming maximum stable revenue is 10 BTC/month
        val maxStableRevenue = 10.0
        return when {
            proposal.expected_monthly_revenue_btc <= 0 -> 0.0
            proposal.expected_monthly_revenue_btc >= maxStableRevenue -> 1.0
            else -> proposal.expected_monthly_revenue_btc / maxStableRevenue
        }
    }
    
    /**
     * Calculate cost efficiency score
     */
    private fun calculateCostEfficiencyScore(proposal: Proposal): Double {
        // Lower cost is generally more efficient
        // Assuming maximum efficient cost is 0.1 ETH
        val minEfficientCost = 0.1
        val maxCost = 100.0
        return when {
            proposal.cost_eth <= 0 -> 0.0
            proposal.cost_eth <= minEfficientCost -> 1.0
            proposal.cost_eth >= maxCost -> 0.0
            else -> 1.0 - (proposal.cost_eth / maxCost)
        }
    }
    
    /**
     * Calculate strategic impact score based on proposal details
     */
    private fun calculateStrategicImpactScore(proposal: Proposal): Double {
        // For now, we'll use a simple heuristic
        // In a real implementation, this would be based on the strategic_impact field
        var score = 0.5 // Default score
        
        // Increase score for proposals with inter-council collaborations
        if (proposal.inter_council_collaborations?.isNotEmpty() == true) {
            score += 0.3
        }
        
        // Increase score for proposals with resource dependencies (shows planning)
        if (proposal.resource_dependencies?.isNotEmpty() == true) {
            score += 0.2
        }
        
        return minOf(1.0, score)
    }
    
    /**
     * Calculate collaboration value score
     */
    private fun calculateCollaborationScore(proposal: Proposal): Double {
        // Score based on number of inter-council collaborations
        val collaborationCount = proposal.inter_council_collaborations?.size ?: 0
        // Max score for 5 or more collaborations
        return when {
            collaborationCount >= 5 -> 1.0
            collaborationCount >= 3 -> 0.7
            collaborationCount >= 1 -> 0.4
            else -> 0.0
        }
    }
    
    /**
     * Calculate risk score based on various factors
     */
    private fun calculateRiskScore(proposal: Proposal): Double {
        var riskScore = 0.0
        
        // High cost increases risk
        if (proposal.cost_eth > 50) {
            riskScore += 0.3
        } else if (proposal.cost_eth > 20) {
            riskScore += 0.1
        }
        
        // Low expected revenue increases risk
        if (proposal.expected_monthly_revenue_btc < 0.1) {
            riskScore += 0.2
        } else if (proposal.expected_monthly_revenue_btc < 0.5) {
            riskScore += 0.1
        }
        
        // Long implementation timeline increases risk
        if (proposal.implementation_timeline_days != null && proposal.implementation_timeline_days > 180) {
            riskScore += 0.2
        }
        
        // Cap risk score at 1.0
        return minOf(1.0, riskScore)
    }
    
    /**
     * Rank proposals based on their scores
     */
    fun rankProposals(proposals: List<Proposal>): List<Proposal> {
        return proposals.sortedByDescending { calculateProposalScore(it) }
    }
    
    /**
     * Get strategic summary for a proposal
     */
    fun getStrategicSummary(proposal: Proposal): String {
        val roi = calculateROI(proposal)
        val score = calculateProposalScore(proposal)
        val collaborations = proposal.inter_council_collaborations?.size ?: 0
        
        return when {
            score > 0.8 -> "High Priority Strategic Initiative"
            score > 0.6 -> "Important Strategic Proposal"
            score > 0.4 -> "Standard Proposal"
            else -> "Low Priority Initiative"
        }
    }
}