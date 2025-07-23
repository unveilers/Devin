import { useState, useEffect } from 'react'
import { TrendingUp, Users, Target, DollarSign, BarChart3 } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts'
import { apiService } from '../services/api'
import { SalesMetrics } from '../types'

export default function AnalyticsModule() {
  const [salesMetrics, setSalesMetrics] = useState<SalesMetrics | null>(null)
  const [pipelineData, setPipelineData] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadAnalytics()
  }, [])

  const loadAnalytics = async () => {
    try {
      const [metricsData, pipelineStageData] = await Promise.all([
        apiService.getSalesMetrics(),
        apiService.getPipelineByStage()
      ])
      setSalesMetrics(metricsData)
      setPipelineData(pipelineStageData)
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  const formatCurrency = (value: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(value)
  }

  const pipelineChartData = pipelineData ? Object.entries(pipelineData).map(([stage, data]: [string, any]) => ({
    stage: stage.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
    count: data.count,
    value: data.value
  })) : []

  const pieChartData = pipelineData ? Object.entries(pipelineData)
    .filter(([_, data]: [string, any]) => data.count > 0)
    .map(([stage, data]: [string, any]) => ({
      name: stage.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase()),
      value: data.count
    })) : []

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D']

  if (loading) {
    return <div className="flex justify-center items-center h-64">Loading analytics...</div>
  }

  if (!salesMetrics) {
    return <div className="flex justify-center items-center h-64">No data available</div>
  }

  return (
    <div className="space-y-6">
      {/* Key Metrics Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Customers</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{salesMetrics.total_customers}</div>
            <p className="text-xs text-muted-foreground">
              {salesMetrics.active_customers} active
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Opportunities</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{salesMetrics.total_opportunities}</div>
            <p className="text-xs text-muted-foreground">
              {salesMetrics.won_opportunities} won
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pipeline Value</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {formatCurrency(salesMetrics.total_pipeline_value)}
            </div>
            <p className="text-xs text-muted-foreground">
              {formatCurrency(salesMetrics.won_value)} won
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Conversion Rate</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{salesMetrics.conversion_rate}%</div>
            <p className="text-xs text-muted-foreground">
              Avg deal: {formatCurrency(salesMetrics.avg_deal_size)}
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid gap-6 md:grid-cols-2">
        {/* Pipeline by Stage Bar Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <BarChart3 className="w-5 h-5 mr-2" />
              Pipeline by Stage
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={pipelineChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis 
                  dataKey="stage" 
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  fontSize={12}
                />
                <YAxis />
                <Tooltip 
                  formatter={(value, name) => [
                    name === 'value' ? formatCurrency(value as number) : value,
                    name === 'value' ? 'Value' : 'Count'
                  ]}
                />
                <Bar dataKey="count" fill="#8884d8" name="count" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Opportunity Distribution Pie Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Opportunity Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={pieChartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {pieChartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Pipeline Value by Stage */}
      <Card>
        <CardHeader>
          <CardTitle>Pipeline Value by Stage</CardTitle>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={pipelineChartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis 
                dataKey="stage" 
                angle={-45}
                textAnchor="end"
                height={80}
                fontSize={12}
              />
              <YAxis tickFormatter={(value) => formatCurrency(value)} />
              <Tooltip 
                formatter={(value) => [formatCurrency(value as number), 'Value']}
              />
              <Bar dataKey="value" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
    </div>
  )
}
