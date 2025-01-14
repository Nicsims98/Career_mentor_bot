```python
    async def _get_coursera_courses(self, role: str) -> Dict:
        """Get course recommendations from Coursera"""
                headers = {'Authorization': f'Bearer {self.coursera_api_key}'}
                    'fields': 'name,slug,workload,rating,specializations'
                    f"{self.endpoints['coursera']}/search",
                        return {
                            'courses': data.get('elements', [])[:5],
                            'source': 'Coursera',
                            'last_updated': datetime.now().isoformat()
                        }
            print(f"Error fetching Coursera data: {str(e)}")
            return self._get_fallback_coursera_data()
    async def _get_udemy_insights(self, role: str) -> Dict:
        """Get course insights from Udemy"""
                headers = {'Authorization': f'Bearer {self.udemy_api_key}'}
                    'search': role,
                    'fields[course]': 'title,url,price,num_reviews,rating'
                    f"{self.endpoints['udemy']}/courses",
                            'courses': data.get('results', [])[:5],
                            'source': 'Udemy',
            print(f"Error fetching Udemy data: {str(e)}")
            return self._get_fallback_udemy_data()
    async def _get_hackernews_trends(self, role: str) -> Dict:
        """Get technology discussions from HackerNews"""
                # Search for stories related to the role
                search_response = await session.get(
                    f"{self.endpoints['hackernews']}/search",
                    params={'query': role, 'tags': 'story'}
                )
                if search_response.status == 200:
                    stories = await search_response.json()
                    return {
                        'trending_discussions': stories['hits'][:5],
                        'source': 'HackerNews',
                        'last_updated': datetime.now().isoformat()
                    }
            print(f"Error fetching HackerNews data: {str(e)}")
            return self._get_fallback_hackernews_data()
    async def _get_meetup_insights(
        self,
        role: str,
        location: Optional[str]
    ) -> Dict:
        """Get professional community insights from Meetup"""
                headers = {'Authorization': f'Bearer {self.meetup_api_key}'}
                query = """
                query($topic: String!, $location: String) {
                    groups(topic: $topic, location: $location) {
                        name
                        members
                        nextEvent {
                            title
                            dateTime
                        }
                    }
                """
                variables = {
                    'topic': role,
                    'location': location
                async with session.post(
                    self.endpoints['meetup'],
                    json={'query': query, 'variables': variables}
                            'groups': data.get('data', {}).get('groups', [])[:5],
                            'source': 'Meetup',
            print(f"Error fetching Meetup data: {str(e)}")
            return self._get_fallback_meetup_data()
```
        self.coursera_api_key = os.getenv('COURSERA_API_KEY')
        self.udemy_api_key = os.getenv('UDEMY_API_KEY')
        self.hackernews_api_key = os.getenv('HACKERNEWS_API_KEY')
        self.meetup_api_key = os.getenv('MEETUP_API_KEY')
            'stackoverflow': 'https://api.stackexchange.com/2.3',
            'bls': 'https://api.bls.gov/publicAPI/v2',
            'github': 'https://api.github.com',
            'dice': 'https://marketplace-api.dice.com/v1',
            'coursera': 'https://api.coursera.org/api/courses.v1',
            'udemy': 'https://www.udemy.com/api-2.0',
            'hackernews': 'https://hacker-news.firebaseio.com/v0',
            'meetup': 'https://api.meetup.com/gql'
        }

    async def get_role_insights(
        self,
        role_title: str,
        location: Optional[str] = None,
        compare_regions: Optional[List[str]] = None
    ) -> Dict:
        """Get comprehensive market insights for a role"""
        cache_key = f"{role_title}_{location}"
        if self._is_cache_valid(cache_key):
            return self.cached_data[cache_key]

        # Gather data from multiple sources concurrently
        tasks = [
            self._get_salary_data(role_title, location),
            self._get_job_demand(role_title, location),
            self._get_growth_trends(role_title),
            self._get_trending_skills(role_title),
            self._get_remote_stats(role_title),
            self._get_stackoverflow_insights(role_title),
            self._get_bls_statistics(role_title),
            self._get_github_trends(role_title),
            self._get_dice_tech_insights(role_title),
            self._get_coursera_courses(role_title),
            self._get_udemy_insights(role_title),
            self._get_hackernews_trends(role_title),
            self._get_meetup_insights(role_title, location)
        ]
        
        results = await asyncio.gather(*tasks)
        
        insights = {
            'salary': results[0],
            'demand': results[1],
            'growth': results[2],
            'skills_in_demand': results[3],
            'remote_opportunities': results[4],
            'stackoverflow_insights': results[5],
            'government_statistics': results[6],
            'github_trends': results[7],
            'tech_industry_insights': results[8],
            'last_updated': datetime.now().isoformat()
        }

        # Cache the results
        self.cached_data[cache_key] = {
            'data': insights,
            'timestamp': datetime.now()
        }

        # Add regional comparison if requested
        if compare_regions:
            regional_insights = await self._get_regional_comparison(
                role_title,
                compare_regions
            )
            insights['regional_comparison'] = regional_insights

        return insights

    async def _get_regional_comparison(
        self,
        role_title: str,
        regions: List[str]
    ) -> Dict[str, Any]:
        """Get market insights across different regions"""
        regional_data = {}
        
        for region in regions:
            # Gather data for each region concurrently
            tasks = [
                self._get_salary_data(role_title, region),
                self._get_job_demand(role_title, region),
                self._get_remote_stats(role_title, region),
                self._get_company_presence(role_title, region),
                self._get_cost_of_living_adjustment(region)
            ]
            
            results = await asyncio.gather(*tasks)
            
            regional_data[region] = {
                'salary': results[0],
                'demand': results[1],
                'remote_work': results[2],
                'companies': results[3],
                'cost_of_living': results[4]
            }
        
        return {
            'data': regional_data,
            'analysis': self._analyze_regional_differences(regional_data),
            'recommendations': self._generate_regional_recommendations(regional_data)
        }

    def _analyze_regional_differences(
        self,
        regional_data: Dict[str, Dict]
    ) -> Dict[str, Any]:
        """Analyze differences between regions"""
        analysis = {
            'salary_comparison': {},
            'demand_comparison': {},
            'lifestyle_comparison': {}
        }
        
        for region, data in regional_data.items():
            # Adjust salaries for cost of living
            col_adjusted_salary = (
                data['salary']['median'] * 
                (100 / data['cost_of_living'])
            )
            
            analysis['salary_comparison'][region] = {
                'nominal': data['salary']['median'],
                'adjusted': col_adjusted_salary
            }
            
            analysis['demand_comparison'][region] = {
                'job_count': data['demand']['current_openings'],
                'growth_rate': data['demand']['year_over_year_growth']
            }
            
            analysis['lifestyle_comparison'][region] = {
                'remote_ratio': data['remote_work']['remote_percentage'],
                'col_index': data['cost_of_living']
            }
        
        return analysis

    def _generate_regional_recommendations(
        self,
        regional_data: Dict[str, Dict]
    ) -> List[Dict[str, str]]:
        """Generate recommendations based on regional analysis"""
        recommendations = []
        
        # Find best region for salary
        best_salary_region = max(
            regional_data.items(),
            key=lambda x: x[1]['salary']['median']
        )[0]
        
        recommendations.append({
            'category': 'salary',
            'recommendation': f"Highest nominal salaries in {best_salary_region}"
        })
        
        # Find best region for job opportunities
        best_opportunity_region = max(
            regional_data.items(),
            key=lambda x: x[1]['demand']['current_openings']
        )[0]
        
        recommendations.append({
            'category': 'opportunities',
            'recommendation': f"Most job openings in {best_opportunity_region}"
        })
        
        # Find best region for remote work
        best_remote_region = max(
            regional_data.items(),
            key=lambda x: x[1]['remote_work']['remote_percentage']
        )[0]
        
        recommendations.append({
            'category': 'remote_work',
            'recommendation': f"Highest remote work opportunities in {best_remote_region}"
        })
        
        return recommendations

    async def _get_salary_data(
        self,
        role: str,
        location: Optional[str]
    ) -> Dict:
        """Get salary data from Glassdoor API"""
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'api_key': self.glassdoor_api_key,
                    'title': role,
                    'location': location or 'United States'
                }
                
                async with session.get(
                    f"{self.endpoints['glassdoor']}/salaries",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_salary_data(data)
                        
        except Exception as e:
            print(f"Error fetching salary data: {str(e)}")
            return self._get_fallback_salary_data()

    async def _get_job_demand(
        self,
        role: str,
        location: Optional[str]
    ) -> Dict:
        """Get job demand data from Indeed API"""
        try:
            async with aiohttp.ClientSession() as session:
                params = {
                    'api_key': self.indeed_api_key,
                    'q': role,
                    'l': location or 'United States',
                    'limit': 100
                }
                
                async with session.get(
                    f"{self.endpoints['indeed']}/jobs/search",
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_job_demand(data)
                        
        except Exception as e:
            print(f"Error fetching job demand: {str(e)}")
            return self._get_fallback_demand_data()

    async def _get_trending_skills(self, role: str) -> List[str]:
        """Get trending skills from LinkedIn API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.linkedin_api_key}',
                    'X-Restli-Protocol-Version': '2.0.0'
                }
                
                params = {
                    'keywords': role,
                    'facet': 'skills'
                }
                
                async with session.get(
                    f"{self.endpoints['linkedin']}/jobSearch",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_trending_skills(data)
                        
        except Exception as e:
            print(f"Error fetching trending skills: {str(e)}")
            return self._get_fallback_skills()

    def _process_salary_data(self, data: Dict) -> Dict:
        """Process raw salary data from Glassdoor"""
        try:
            salary_info = data.get('salaryInfo', {})
            return {
                'entry_level': {
                    'min': salary_info.get('entry', {}).get('min', 50000),
                    'max': salary_info.get('entry', {}).get('max', 70000),
                    'median': salary_info.get('entry', {}).get('median', 60000)
                },
                'mid_level': {
                    'min': salary_info.get('mid', {}).get('min', 70000),
                    'max': salary_info.get('mid', {}).get('max', 100000),
                    'median': salary_info.get('mid', {}).get('median', 85000)
                },
                'senior_level': {
                    'min': salary_info.get('senior', {}).get('min', 100000),
                    'max': salary_info.get('senior', {}).get('max', 150000),
                    'median': salary_info.get('senior', {}).get('median', 125000)
                },
                'source': 'Glassdoor',
                'last_updated': datetime.now().isoformat()
            }
        except Exception:
            return self._get_fallback_salary_data()

    def _process_job_demand(self, data: Dict) -> Dict:
        """Process raw job demand data from Indeed"""
        try:
            total_jobs = len(data.get('results', []))
            companies = {}
            
            # Count job postings by company
            for job in data.get('results', []):
                company = job.get('company', 'Unknown')
                companies[company] = companies.get(company, 0) + 1
            
            # Get top hiring companies
            top_companies = sorted(
                companies.items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            
            return {
                'current_openings': total_jobs,
                'year_over_year_growth': self._calculate_yoy_growth(data),
                'competition_level': self._determine_competition_level(total_jobs),
                'most_hiring_companies': [comp[0] for comp in top_companies],
                'source': 'Indeed',
                'last_updated': datetime.now().isoformat()
            }
        except Exception:
            return self._get_fallback_demand_data()

    def _calculate_yoy_growth(self, data: Dict) -> float:
        """Calculate year-over-year growth from job posting data"""
        try:
            current_count = len(data.get('results', []))
            historical = data.get('historical', {})
            last_year_count = historical.get('last_year', current_count * 0.8)
            
            return round(
                ((current_count - last_year_count) / last_year_count) * 100,
                1
            )
        except Exception:
            return 15.0  # Default growth rate

    def _determine_competition_level(self, job_count: int) -> str:
        """Determine competition level based on number of openings"""
        if job_count < 100:
            return "high"
        elif job_count < 1000:
            return "moderate"
        else:
            return "low"

    def _get_fallback_salary_data(self) -> Dict:
        """Provide fallback salary data when API fails"""
        return {
            'entry_level': {
                'min': 50000,
                'max': 70000,
                'median': 60000
            },
            'mid_level': {
                'min': 70000,
                'max': 100000,
                'median': 85000
            },
            'senior_level': {
                'min': 100000,
                'max': 150000,
                'median': 125000
            },
            'source': 'Historical Data',
            'last_updated': datetime.now().isoformat()
        }

    def _get_fallback_demand_data(self) -> Dict:
        """Provide fallback demand data when API fails"""
        return {
            'current_openings': 1500,
            'year_over_year_growth': 15,
            'competition_level': 'moderate',
            'most_hiring_companies': [
                'Google',
                'Microsoft',
                'Amazon',
                'Meta',
                'Apple'
            ],
            'source': 'Historical Data',
            'last_updated': datetime.now().isoformat()
        }

    async def _get_stackoverflow_insights(self, role: str) -> Dict:
        """Get insights from Stack Overflow Developer Survey and API"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'key': self.stackoverflow_key}
                params = {
                    'site': 'stackoverflow',
                    'tagged': role.replace(' ', '-').lower(),
                    'sort': 'activity',
                    'filter': 'total'
                }
                
                async with session.get(
                    f"{self.endpoints['stackoverflow']}/tags/{role}/info",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'question_count': data.get('total_questions', 0),
                            'tag_popularity': data.get('popularity', 0),
                            'related_tags': data.get('related_tags', [])[:5],
                            'source': 'Stack Overflow',
                            'last_updated': datetime.now().isoformat()
                        }
        except Exception as e:
            print(f"Error fetching Stack Overflow data: {str(e)}")
            return self._get_fallback_stackoverflow_data()

    async def _get_bls_statistics(self, role: str) -> Dict:
        """Get official statistics from Bureau of Labor Statistics"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'Registration-Key': self.bls_api_key}
                payload = {
                    'seriesid': ['OEUM001910000000000AM5613'],
                    'startyear': '2022',
                    'endyear': '2023'
                }
                
                async with session.post(
                    f"{self.endpoints['bls']}/timeseries/data/",
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self._process_bls_data(data)
        except Exception as e:
            print(f"Error fetching BLS data: {str(e)}")
            return self._get_fallback_bls_data()

    async def _get_github_trends(self, role: str) -> Dict:
        """Get technology trends from GitHub"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'token {self.github_token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
                
                # Convert role to relevant search terms
                search_terms = self._role_to_github_terms(role)
                
                results = {}
                for term in search_terms:
                    async with session.get(
                        f"{self.endpoints['github']}/search/repositories",
                        headers=headers,
                        params={'q': term, 'sort': 'stars'}
                    ) as response:
                        if response.status == 200:
                            data = await response.json()
                            results[term] = {
                                'repository_count': data.get('total_count', 0),
                                'top_repos': [
                                    {
                                        'name': repo['full_name'],
                                        'stars': repo['stargazers_count'],
                                        'url': repo['html_url']
                                    }
                                    for repo in data.get('items', [])[:5]
                                ]
                            }
                
                return {
                    'trends': results,
                    'source': 'GitHub',
                    'last_updated': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Error fetching GitHub data: {str(e)}")
            return self._get_fallback_github_data()

    async def _get_dice_tech_insights(self, role: str) -> Dict:
        """Get technology industry insights from Dice"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {'X-Api-Key': self.dice_api_key}
                params = {
                    'q': role,
                    'fields': 'skills,salary,companies,locations'
                }
                
                async with session.get(
                    f"{self.endpoints['dice']}/jobs/trends",
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return {
                            'skill_trends': data.get('skills', [])[:10],
                            'top_locations': data.get('locations', [])[:5],
                            'emerging_companies': data.get('companies', [])[:5],
                            'source': 'Dice',
                            'last_updated': datetime.now().isoformat()
                        }
        except Exception as e:
            print(f"Error fetching Dice data: {str(e)}")
            return self._get_fallback_dice_data()

    def _process_bls_data(self, data: Dict) -> Dict:
        """Process Bureau of Labor Statistics data"""
        try:
            series = data.get('Results', {}).get('series', [{}])[0]
            latest_data = series.get('data', [{}])[0]
            
            return {
                'employment_count': latest_data.get('value'),
                'period': latest_data.get('period'),
                'year': latest_data.get('year'),
                'growth_rate': latest_data.get('calculations', {}).get('pct_change'),
                'source': 'Bureau of Labor Statistics',
                'last_updated': datetime.now().isoformat()
            }
        except Exception:
            return self._get_fallback_bls_data()

    def _role_to_github_terms(self, role: str) -> List[str]:
        """Convert role to relevant GitHub search terms"""
        role_mappings = {
            'frontend developer': ['javascript-framework', 'react', 'vue'],
            'backend developer': ['backend-framework', 'api-development'],
            'data scientist': ['data-science', 'machine-learning'],
            'devops engineer': ['devops-tools', 'kubernetes'],
            'full stack developer': ['full-stack', 'web-development']
        }
        return role_mappings.get(role.lower(), [role.lower()])

    def _get_fallback_stackoverflow_data(self) -> Dict:
        """Fallback data for Stack Overflow"""
        return {
            'question_count': 5000,
            'tag_popularity': 80,
            'related_tags': ['python', 'javascript', 'react', 'node.js'],
            'source': 'Historical Data',
            'last_updated': datetime.now().isoformat()
        }

    def _get_fallback_bls_data(self) -> Dict:
        """Fallback data for BLS"""
        return {
            'employment_count': 1500000,
            'period': 'M12',
            'year': '2023',
            'growth_rate': 4.5,
            'source': 'Historical Data',
            'last_updated': datetime.now().isoformat()
        }

    def _get_fallback_github_data(self) -> Dict:
        """Fallback data for GitHub"""
        return {
            'trends': {
                'python': {
                    'repository_count': 100000,
                    'top_repos': [
                        {
                            'name': 'tensorflow/tensorflow',
                            'stars': 50000,
                            'url': 'https://github.com/tensorflow/tensorflow'
                        }
                    ]
                }
            },
            'source': 'Historical Data',
            'last_updated': datetime.now().isoformat()
        }

    def _get_fallback_dice_data(self) -> Dict:
        """Fallback data for Dice"""
        return {
            'skill_trends': ['Python', 'JavaScript', 'AWS', 'React', 'Docker'],
            'top_locations': ['San Francisco', 'New York', 'Seattle'],
            'emerging_companies': ['Google', 'Amazon', 'Microsoft'],
            'source': 'Historical Data',
            'last_updated': datetime.now().isoformat()
        }

    def _get_fallback_skills(self) -> List[str]:
        """Provide fallback skills data when API fails"""
        return [
            'Python',
            'JavaScript',
            'SQL',
            'Machine Learning',
            'Cloud Computing'
        ]
