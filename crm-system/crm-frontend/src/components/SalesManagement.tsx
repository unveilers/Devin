import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, DollarSign, Calendar, TrendingUp } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog'
import { Label } from '@/components/ui/label'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { Textarea } from '@/components/ui/textarea'
import { apiService } from '../services/api'
import { Opportunity, Customer } from '../types'

export default function SalesManagement() {
  const [opportunities, setOpportunities] = useState<Opportunity[]>([])
  const [customers, setCustomers] = useState<Customer[]>([])
  const [loading, setLoading] = useState(true)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingOpportunity, setEditingOpportunity] = useState<Opportunity | null>(null)
  const [formData, setFormData] = useState<Partial<Opportunity>>({
    customer_id: 0,
    title: '',
    description: '',
    value: 0,
    stage: 'lead',
    probability: 0,
    expected_close_date: ''
  })

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      const [opportunitiesData, customersData] = await Promise.all([
        apiService.getOpportunities(),
        apiService.getCustomers()
      ])
      setOpportunities(opportunitiesData)
      setCustomers(customersData)
    } catch (error) {
      console.error('Failed to load data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.customer_id || formData.customer_id === 0) {
      alert('Please select a customer')
      return
    }
    if (!formData.title?.trim()) {
      alert('Please enter a title')
      return
    }
    if (!formData.value || formData.value <= 0) {
      alert('Please enter a valid value')
      return
    }
    
    try {
      if (editingOpportunity) {
        await apiService.updateOpportunity(editingOpportunity.id!, formData)
      } else {
        await apiService.createOpportunity(formData)
      }
      await loadData()
      setIsDialogOpen(false)
      setEditingOpportunity(null)
      setFormData({
        customer_id: 0,
        title: '',
        description: '',
        value: 0,
        stage: 'lead',
        probability: 0,
        expected_close_date: ''
      })
    } catch (error) {
      console.error('Failed to save opportunity:', error)
      alert('Failed to save opportunity. Please try again.')
    }
  }

  const handleEdit = (opportunity: Opportunity) => {
    setEditingOpportunity(opportunity)
    setFormData({
      ...opportunity,
      expected_close_date: opportunity.expected_close_date ? opportunity.expected_close_date.split('T')[0] : ''
    })
    setIsDialogOpen(true)
  }

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this opportunity?')) {
      try {
        await apiService.deleteOpportunity(id)
        await loadData()
      } catch (error) {
        console.error('Failed to delete opportunity:', error)
      }
    }
  }

  const getStageColor = (stage: string) => {
    switch (stage) {
      case 'lead': return 'bg-gray-100 text-gray-800'
      case 'qualified': return 'bg-blue-100 text-blue-800'
      case 'proposal': return 'bg-yellow-100 text-yellow-800'
      case 'negotiation': return 'bg-orange-100 text-orange-800'
      case 'closed_won': return 'bg-green-100 text-green-800'
      case 'closed_lost': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getCustomerName = (customerId: number) => {
    const customer = customers.find(c => c.id === customerId)
    return customer ? `${customer.first_name} ${customer.last_name}` : 'Unknown'
  }

  const groupedOpportunities = opportunities.reduce((acc, opp) => {
    if (!acc[opp.stage]) {
      acc[opp.stage] = []
    }
    acc[opp.stage].push(opp)
    return acc
  }, {} as Record<string, Opportunity[]>)

  const stages = ['lead', 'qualified', 'proposal', 'negotiation', 'closed_won', 'closed_lost']

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading opportunities...</div>
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h3 className="text-lg font-semibold">Sales Pipeline</h3>
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => {
              setEditingOpportunity(null)
              setFormData({
                customer_id: 0,
                title: '',
                description: '',
                value: 0,
                stage: 'lead',
                probability: 0,
                expected_close_date: ''
              })
            }}>
              <Plus className="w-4 h-4 mr-2" />
              Add Opportunity
            </Button>
          </DialogTrigger>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>
                {editingOpportunity ? 'Edit Opportunity' : 'Add New Opportunity'}
              </DialogTitle>
            </DialogHeader>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="customer_id">Customer</Label>
                <Select value={formData.customer_id?.toString()} onValueChange={(value) => setFormData({ ...formData, customer_id: parseInt(value) })}>
                  <SelectTrigger>
                    <SelectValue placeholder="Select customer" />
                  </SelectTrigger>
                  <SelectContent>
                    {customers.map((customer) => (
                      <SelectItem key={customer.id} value={customer.id!.toString()}>
                        {customer.first_name} {customer.last_name}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="title">Title</Label>
                <Input
                  id="title"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  required
                />
              </div>
              <div>
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  value={formData.description}
                  onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                />
              </div>
              <div>
                <Label htmlFor="value">Value ($)</Label>
                <Input
                  id="value"
                  type="number"
                  value={formData.value}
                  onChange={(e) => setFormData({ ...formData, value: parseFloat(e.target.value) })}
                  required
                />
              </div>
              <div>
                <Label htmlFor="stage">Stage</Label>
                <Select value={formData.stage} onValueChange={(value) => setFormData({ ...formData, stage: value as any })}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="lead">Lead</SelectItem>
                    <SelectItem value="qualified">Qualified</SelectItem>
                    <SelectItem value="proposal">Proposal</SelectItem>
                    <SelectItem value="negotiation">Negotiation</SelectItem>
                    <SelectItem value="closed_won">Closed Won</SelectItem>
                    <SelectItem value="closed_lost">Closed Lost</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              <div>
                <Label htmlFor="probability">Probability (%)</Label>
                <Input
                  id="probability"
                  type="number"
                  min="0"
                  max="100"
                  value={formData.probability}
                  onChange={(e) => setFormData({ ...formData, probability: parseInt(e.target.value) })}
                />
              </div>
              <div>
                <Label htmlFor="expected_close_date">Expected Close Date</Label>
                <Input
                  id="expected_close_date"
                  type="date"
                  value={formData.expected_close_date}
                  onChange={(e) => setFormData({ ...formData, expected_close_date: e.target.value })}
                />
              </div>
              <div className="flex justify-end space-x-2">
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit">
                  {editingOpportunity ? 'Update' : 'Create'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        {stages.map((stage) => (
          <div key={stage} className="bg-gray-50 rounded-lg p-4">
            <h4 className="font-semibold mb-3 capitalize text-center">
              {stage.replace('_', ' ')}
            </h4>
            <div className="space-y-3">
              {(groupedOpportunities[stage] || []).map((opportunity) => (
                <Card key={opportunity.id} className="hover:shadow-md transition-shadow">
                  <CardHeader className="pb-2">
                    <div className="flex justify-between items-start">
                      <CardTitle className="text-sm font-medium">
                        {opportunity.title}
                      </CardTitle>
                      <div className="flex space-x-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleEdit(opportunity)}
                        >
                          <Edit className="w-3 h-3" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleDelete(opportunity.id!)}
                        >
                          <Trash2 className="w-3 h-3" />
                        </Button>
                      </div>
                    </div>
                  </CardHeader>
                  <CardContent className="space-y-2">
                    <div className="text-xs text-gray-600">
                      {getCustomerName(opportunity.customer_id)}
                    </div>
                    <div className="flex items-center text-sm font-semibold text-green-600">
                      <DollarSign className="w-4 h-4 mr-1" />
                      ${opportunity.value.toLocaleString()}
                    </div>
                    <div className="flex items-center text-xs text-gray-500">
                      <TrendingUp className="w-3 h-3 mr-1" />
                      {opportunity.probability}% probability
                    </div>
                    {opportunity.expected_close_date && (
                      <div className="flex items-center text-xs text-gray-500">
                        <Calendar className="w-3 h-3 mr-1" />
                        {new Date(opportunity.expected_close_date).toLocaleDateString()}
                      </div>
                    )}
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        ))}
      </div>

      {opportunities.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500">No opportunities found</p>
        </div>
      )}
    </div>
  )
}
