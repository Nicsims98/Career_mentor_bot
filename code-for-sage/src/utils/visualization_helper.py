"""
Data visualization utilities for market insights with interactive features
"""

import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List, Any, Optional
import pandas as pd
import json

class MarketVisualizer:
    def __init__(self):
        self.color_scheme = {
            'primary': '#2C3E50',
            'secondary': '#E74C3C',
            'accent': '#3498DB',
            'background': '#ECF0F1'
        }
        
        # Default interactive settings
        self.default_interactive_config = {
            'scrollZoom': True,
            'displayModeBar': True,
            'editable': True,
            'showLink': False,
            'displaylogo': False
        }

    def create_interactive_salary_comparison(
        self,
        salary_data: Dict[str, Any],
        regions: List[str],
        show_outliers: bool = True,
        add_annotations: bool = True
    ) -> str:
        """Create interactive salary comparison chart across regions"""
        df = pd.DataFrame(salary_data)
        
        fig = go.Figure()
        
        for region in regions:
            fig.add_trace(go.Box(
                y=df[df['region'] == region]['salary'],
                name=region,
                boxpoints='all' if show_outliers else False,
                jitter=0.3,
                pointpos=-1.8,
                hovertemplate=(
                    '<b>Salary</b>: $%{y:,.0f}<br>'
                    '<b>Region</b>: %{x}<br>'
                    '<extra></extra>'
                )
            ))
        
        if add_annotations:
            for region in regions:
                median = df[df['region'] == region]['salary'].median()
                fig.add_annotation(
                    x=region,
                    y=median,
                    text=f'Median: ${median:,.0f}',
                    showarrow=True,
                    arrowhead=1
                )
        
        fig.update_layout(
            title={
                'text': 'Salary Distribution by Region',
                'x': 0.5,
                'xanchor': 'center'
            },
            yaxis_title='Annual Salary (USD)',
            template='plotly_white',
            showlegend=True,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            ),
            # Add range slider
            xaxis=dict(
                rangeslider=dict(visible=True)
            ),
            updatemenus=[
                dict(
                    type="buttons",
                    direction="left",
                    buttons=list([
                        dict(
                            args=[{"visible": [True] * len(regions)}],
                            label="Show All",
                            method="update"
                        ),
                        dict(
                            args=[{"visible": [False] * len(regions)}],
                            label="Hide All",
                            method="update"
                        )
                    ]),
                    pad={"r": 10, "t": 10},
                    showactive=True,
                    x=0.11,
                    xanchor="left",
                    y=1.1,
                    yanchor="top"
                ),
            ]
        )
        
        return fig.to_json()

    def create_interactive_skill_heatmap(
        self,
        skill_data: Dict[str, Dict[str, float]],
        regions: List[str],
        colorscale: Optional[str] = 'Viridis'
    ) -> str:
        """Create interactive heatmap of skill demand across regions"""
        df = pd.DataFrame(skill_data)
        
        fig = go.Figure(data=go.Heatmap(
            z=df.values,
            x=df.columns,
            y=df.index,
            colorscale=colorscale,
            hoverongaps=False,
            hovertemplate=(
                '<b>Region</b>: %{x}<br>'
                '<b>Skill</b>: %{y}<br>'
                '<b>Demand</b>: %{z:.1f}%<br>'
                '<extra></extra>'
            )
        ))
        
        # Add colorscale selector
        updatemenus = [
            dict(
                buttons=list([
                    dict(
                        args=[{'colorscale': 'Viridis'}],
                        label='Viridis',
                        method='restyle'
                    ),
                    dict(
                        args=[{'colorscale': 'RdBu'}],
                        label='RdBu',
                        method='restyle'
                    ),
                    dict(
                        args=[{'colorscale': 'Jet'}],
                        label='Jet',
                        method='restyle'
                    )
                ]),
                direction='down',
                showactive=True,
                x=0.1,
                xanchor='left',
                y=1.1,
                yanchor='top'
            )
        ]
        
        fig.update_layout(
            title='Skill Demand Heatmap by Region',
            xaxis_title='Region',
            yaxis_title='Skill',
            template='plotly_white',
            updatemenus=updatemenus,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        return fig.to_json()

    def create_interactive_trend_chart(
        self,
        trend_data: Dict[str, List[float]],
        regions: List[str],
        time_range: Optional[str] = 'YTD'
    ) -> str:
        """Create interactive trend chart with time range selector"""
        df = pd.DataFrame(trend_data)
        
        fig = go.Figure()
        
        for region in regions:
            fig.add_trace(go.Scatter(
                x=df.index,
                y=df[region],
                name=region,
                mode='lines+markers',
                hovertemplate=(
                    '<b>Date</b>: %{x|%B %Y}<br>'
                    '<b>Growth</b>: %{y:.1f}%<br>'
                    '<extra></extra>'
                )
            ))
        
        # Add range selector
        fig.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1, label="1m", step="month", stepmode="backward"),
                        dict(count=6, label="6m", step="month", stepmode="backward"),
                        dict(count=1, label="YTD", step="year", stepmode="todate"),
                        dict(count=1, label="1y", step="year", stepmode="backward"),
                        dict(step="all", label="All")
                    ])
                ),
                rangeslider=dict(visible=True),
                type="date"
            )
        )
        
        # Add trend line toggle
        updatemenus = [
            dict(
                type="buttons",
                direction="left",
                buttons=list([
                    dict(
                        args=[{"visible": [True] * len(regions)}],
                        label="Show All",
                        method="update"
                    ),
                    dict(
                        args=[{"visible": [False] * len(regions)}],
                        label="Hide All",
                        method="update"
                    )
                ]),
                pad={"r": 10, "t": 10},
                showactive=True,
                x=0.11,
                xanchor="left",
                y=1.1,
                yanchor="top"
            )
        ]
        
        fig.update_layout(
            title='Growth Trends by Region',
            yaxis_title='Growth Rate (%)',
            template='plotly_white',
            showlegend=True,
            updatemenus=updatemenus,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        return fig.to_json()

    def create_interactive_tech_radar(
        self,
        tech_data: Dict[str, Dict[str, float]],
        regions: List[str],
        enable_animation: bool = True
    ) -> str:
        """Create interactive radar chart of tech stack popularity"""
        fig = go.Figure()
        
        for i, region in enumerate(regions):
            fig.add_trace(go.Scatterpolar(
                r=list(tech_data[region].values()),
                theta=list(tech_data[region].keys()),
                fill='toself',
                name=region,
                hovertemplate=(
                    '<b>Technology</b>: %{theta}<br>'
                    '<b>Popularity</b>: %{r:.1f}%<br>'
                    '<extra></extra>'
                )
            ))
        
        if enable_animation:
            frames = []
            for i in range(len(regions)):
                frame_data = []
                for j, region in enumerate(regions):
                    visible = True if j == i else False
                    frame_data.append(go.Scatterpolar(
                        visible=visible,
                        r=list(tech_data[region].values()),
                        theta=list(tech_data[region].keys()),
                        fill='toself',
                        name=region
                    ))
                frames.append(go.Frame(data=frame_data, name=str(i)))
            
            fig.frames = frames
            
            # Add animation buttons
            fig.update_layout(
                updatemenus=[dict(
                    type='buttons',
                    showactive=False,
                    buttons=[
                        dict(label='Play',
                             method='animate',
                             args=[None, {'frame': {'duration': 500, 'redraw': True},
                                        'fromcurrent': True}]),
                        dict(label='Pause',
                             method='animate',
                             args=[[None], {'frame': {'duration': 0, 'redraw': False},
                                          'mode': 'immediate',
                                          'transition': {'duration': 0}}])
                    ]
                )]
            )
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title='Tech Stack Popularity by Region',
            showlegend=True,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial"
            )
        )
        
        return fig.to_json()

    def export_visualization(
        self,
        fig_json: str,
        format: str = 'html',
        filename: Optional[str] = None
    ) -> str:
        """Export visualization to various formats"""
        fig = go.Figure(json.loads(fig_json))
        
        if format == 'html':
            if not filename:
                filename = 'visualization.html'
            fig.write_html(
                filename,
                config=self.default_interactive_config,
                include_plotlyjs=True,
                full_html=True
            )
        elif format == 'png':
            if not filename:
                filename = 'visualization.png'
            fig.write_image(filename)
        elif format == 'svg':
            if not filename:
                filename = 'visualization.svg'
            fig.write_image(filename)
        elif format == 'pdf':
            if not filename:
                filename = 'visualization.pdf'
            fig.write_image(filename)
            
        return filename
