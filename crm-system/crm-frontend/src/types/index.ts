export interface Customer {
  id?: number
  first_name: string
  last_name: string
  email: string
  phone?: string
  company?: string
  status: 'active' | 'inactive' | 'prospect'
  created_at?: string
  updated_at?: string
}

export interface Opportunity {
  id?: number
  customer_id: number
  title: string
  description?: string
  value: number
  stage: 'lead' | 'qualified' | 'proposal' | 'negotiation' | 'closed_won' | 'closed_lost'
  probability: number
  expected_close_date?: string
  created_at?: string
  updated_at?: string
}

export interface Campaign {
  id?: number
  name: string
  description?: string
  status: 'draft' | 'active' | 'paused' | 'completed'
  budget?: number
  start_date?: string
  end_date?: string
  created_at?: string
  updated_at?: string
}

export interface Activity {
  id?: number
  customer_id: number
  opportunity_id?: number
  type: string
  subject: string
  description?: string
  created_at?: string
}

export interface SalesMetrics {
  total_customers: number
  active_customers: number
  total_opportunities: number
  total_pipeline_value: number
  won_opportunities: number
  won_value: number
  conversion_rate: number
  avg_deal_size: number
}
