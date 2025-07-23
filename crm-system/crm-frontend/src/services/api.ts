const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

class ApiService {
  private async request<T>(endpoint: string, options?: RequestInit): Promise<T> {
    const url = `${API_BASE_URL}${endpoint}`
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
      ...options,
    })

    if (!response.ok) {
      throw new Error(`API request failed: ${response.statusText}`)
    }

    return response.json()
  }

  async getCustomers() {
    return this.request('/api/customers')
  }

  async getCustomer(id: number) {
    return this.request(`/api/customers/${id}`)
  }

  async createCustomer(customer: any) {
    return this.request('/api/customers', {
      method: 'POST',
      body: JSON.stringify(customer),
    })
  }

  async updateCustomer(id: number, customer: any) {
    return this.request(`/api/customers/${id}`, {
      method: 'PUT',
      body: JSON.stringify(customer),
    })
  }

  async deleteCustomer(id: number) {
    return this.request(`/api/customers/${id}`, {
      method: 'DELETE',
    })
  }

  async getOpportunities() {
    return this.request('/api/opportunities')
  }

  async getOpportunity(id: number) {
    return this.request(`/api/opportunities/${id}`)
  }

  async createOpportunity(opportunity: any) {
    return this.request('/api/opportunities', {
      method: 'POST',
      body: JSON.stringify(opportunity),
    })
  }

  async updateOpportunity(id: number, opportunity: any) {
    return this.request(`/api/opportunities/${id}`, {
      method: 'PUT',
      body: JSON.stringify(opportunity),
    })
  }

  async deleteOpportunity(id: number) {
    return this.request(`/api/opportunities/${id}`, {
      method: 'DELETE',
    })
  }

  async getCustomerOpportunities(customerId: number) {
    return this.request(`/api/customers/${customerId}/opportunities`)
  }

  async getCampaigns() {
    return this.request('/api/campaigns')
  }

  async getCampaign(id: number) {
    return this.request(`/api/campaigns/${id}`)
  }

  async createCampaign(campaign: any) {
    return this.request('/api/campaigns', {
      method: 'POST',
      body: JSON.stringify(campaign),
    })
  }

  async updateCampaign(id: number, campaign: any) {
    return this.request(`/api/campaigns/${id}`, {
      method: 'PUT',
      body: JSON.stringify(campaign),
    })
  }

  async deleteCampaign(id: number) {
    return this.request(`/api/campaigns/${id}`, {
      method: 'DELETE',
    })
  }

  async getActivities() {
    return this.request('/api/activities')
  }

  async createActivity(activity: any) {
    return this.request('/api/activities', {
      method: 'POST',
      body: JSON.stringify(activity),
    })
  }

  async getCustomerActivities(customerId: number) {
    return this.request(`/api/customers/${customerId}/activities`)
  }

  async getSalesMetrics() {
    return this.request('/api/analytics/sales-metrics')
  }

  async getPipelineByStage() {
    return this.request('/api/analytics/pipeline-by-stage')
  }
}

export const apiService = new ApiService()
