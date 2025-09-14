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
        // Base ROI score (40% weight)
        val roi = calculateROI(proposal)
        val roiScore = normalizeROI(roi) * 0.4
        
        // Revenue stability score (30% weight)
        val revenueStabilityScore = calculateRevenueStabilityScore(proposal) * 0.3
        
        // Cost efficiency score (20% weight)
        val costEfficiencyScore = calculateCostEfficiencyScore(proposal) * 0.2
        
        // Risk score (10% weight)
        val riskScore = calculateRiskScore(proposal) * 0.1
        
        return max(0.0, roiScore + revenueStabilityScore + costEfficiencyScore - riskScore)
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
        
        // Cap risk score at 1.0
        return minOf(1.0, riskScore)
    }
    
    /**
     * Rank proposals based on their scores
     */
    fun rankProposals(proposals: List<Proposal>): List<Proposal> {
        return proposals.sortedByDescending { calculateProposalScore(it) }
    }
}