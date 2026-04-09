/**
 * Validation issue found during rule or AI validation
 */
export interface ValidationIssue {
  field: string;
  issueType: string;
  severity: 'low' | 'medium' | 'high';
  detectedBy: 'rule_layer' | 'ai_layer';
  explanation: string;
  suggestedCorrection?: string;
}

/**
 * Complete validation report
 */
export interface ValidationReport {
  isValid: boolean;
  totalIssues: number;
  issues: ValidationIssue[];
  validationConfidence: number;
  overallAssessment?: string;
  requiresHumanReview: boolean;
}

/**
 * Rule-based validation result
 */
export interface RuleValidationResult {
  isValid: boolean;
  issues: ValidationIssue[];
  confidence: number;
}

/**
 * AI-layer validation result
 */
export interface AIValidationResult {
  additionalIssues: ValidationIssue[];
  overallAssessment: string;
  requiresHumanReview: boolean;
}
