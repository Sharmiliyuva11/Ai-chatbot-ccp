import requests
import json
from typing import List, Dict, Any
import os
from flask import current_app

class LocalSupportService:
    """Service for finding local mental health support services"""

    def __init__(self):
        # You can add API keys for external services here
        self.google_api_key = os.getenv('GOOGLE_PLACES_API_KEY', '')
        self.open_data_api_key = os.getenv('OPEN_DATA_API_KEY', '')

    def search_mental_health_services(self, location: str, service_type: str = 'all') -> Dict[str, Any]:
        """
        Search for mental health services in a given location

        Args:
            location: City name or zip code
            service_type: Type of service (therapists, hospitals, support_groups, etc.)

        Returns:
            Dictionary containing search results
        """
        try:
            results = []

            # Normalize location for better matching
            location_lower = location.lower().strip()

            # Get static data for various cities
            city_services = self._get_city_mental_health_services(location_lower)

            if city_services:
                results.extend(city_services)

            # Try Google Places API if key is available and no static results found
            if self.google_api_key and not results:
                google_results = self._search_google_places(location, service_type)
                results.extend(google_results)

            # If still no results, try broader search
            if not results and self.google_api_key:
                # Try searching without specific service type
                google_results = self._search_google_places(location, 'all')
                results.extend(google_results)

            # Filter by service type
            if service_type != 'all':
                results = [r for r in results if r.get('type', '').lower() == service_type.lower()]

            return {
                'success': True,
                'location': location,
                'service_type': service_type,
                'results': results,
                'total': len(results)
            }

        except Exception as e:
            current_app.logger.error(f"Error searching local support: {str(e)}")
            return {
                'success': False,
                'error': 'Failed to search local support services',
                'results': [],
                'total': 0
            }

    def _get_city_mental_health_services(self, location: str) -> List[Dict[str, Any]]:
        """Get mental health services for a specific city"""
        city_data = {
            'delhi': self._get_delhi_mental_health_services(),
            'new delhi': self._get_delhi_mental_health_services(),
            'delhi ncr': self._get_delhi_mental_health_services(),
            'chennai': self._get_chennai_mental_health_services(),
            'mumbai': self._get_mumbai_mental_health_services(),
            'bangalore': self._get_bangalore_mental_health_services(),
            'kolkata': self._get_kolkata_mental_health_services(),
            'pune': self._get_pune_mental_health_services(),
            'hyderabad': self._get_hyderabad_mental_health_services(),
            'ahmedabad': self._get_ahmedabad_mental_health_services()
        }

        return city_data.get(location, [])

    def _get_delhi_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Delhi"""
        return [
            {
                'id': 'delhi_mh_001',
                'name': 'All India Institute of Medical Sciences (AIIMS) - Psychiatry Department',
                'type': 'hospital',
                'address': 'Ansari Nagar, New Delhi, Delhi 110029',
                'phone': '+91-11-26588500',
                'services': ['Psychiatric consultation', 'Mental health treatment', 'Emergency care'],
                'specialties': ['Psychiatry', 'Psychology', 'Mental Health'],
                'rating': 4.5,
                'coordinates': {'lat': 28.5672, 'lng': 77.2100},
                'website': 'https://www.aiims.edu/',
                'description': 'Premier medical institution providing comprehensive mental health services'
            },
            {
                'id': 'delhi_mh_002',
                'name': 'Institute of Human Behaviour and Allied Sciences (IHBAS)',
                'type': 'hospital',
                'address': 'Dilshad Garden, New Delhi, Delhi 110095',
                'phone': '+91-11-22114021',
                'services': ['Mental health treatment', 'Psychiatric care', 'Rehabilitation'],
                'specialties': ['Psychiatry', 'Neurology', 'Psychology'],
                'rating': 4.3,
                'coordinates': {'lat': 28.6758, 'lng': 77.3150},
                'website': 'https://www.ihbas.delhigovt.nic.in/',
                'description': 'Specialized mental health institute offering comprehensive care'
            },
            {
                'id': 'delhi_mh_003',
                'name': 'Lady Hardinge Medical College - Psychiatry Department',
                'type': 'hospital',
                'address': 'Connaught Place, New Delhi, Delhi 110001',
                'phone': '+91-11-23363728',
                'services': ['Psychiatric consultation', 'Mental health counseling'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 4.2,
                'coordinates': {'lat': 28.6304, 'lng': 77.2198},
                'website': 'https://lhmc-hosp.gov.in/',
                'description': 'Medical college providing mental health services'
            },
            {
                'id': 'delhi_mh_004',
                'name': 'VIMHANS Hospital',
                'type': 'hospital',
                'address': '1, Institutional Area, Nehru Nagar, New Delhi, Delhi 110065',
                'phone': '+91-11-66172255',
                'services': ['Mental health treatment', 'Psychiatric care', 'Rehabilitation'],
                'specialties': ['Psychiatry', 'Psychology', 'De-addiction'],
                'rating': 4.4,
                'coordinates': {'lat': 28.5439, 'lng': 77.2500},
                'website': 'https://vimhans.com/',
                'description': 'Specialized mental health and psychiatry hospital'
            },
            {
                'id': 'delhi_mh_005',
                'name': 'Max Healthcare - Saket Mental Health Unit',
                'type': 'hospital',
                'address': '1,2, Press Enclave Road, Saket, New Delhi, Delhi 110017',
                'phone': '+91-11-26515050',
                'services': ['Mental health consultation', 'Psychiatric treatment'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 4.1,
                'coordinates': {'lat': 28.5273, 'lng': 77.2198},
                'website': 'https://www.maxhealthcare.in/',
                'description': 'Multi-specialty hospital with mental health services'
            },
            {
                'id': 'delhi_mh_006',
                'name': 'Fortis Healthcare - Vasant Kunj Mental Health',
                'type': 'hospital',
                'address': 'Sector B, Pocket 1, Aruna Asaf Ali Marg, Vasant Kunj, New Delhi, Delhi 110070',
                'phone': '+91-11-42776222',
                'services': ['Mental health treatment', 'Psychiatric care'],
                'specialties': ['Psychiatry', 'Psychology'],
                'rating': 4.0,
                'coordinates': {'lat': 28.5355, 'lng': 77.1457},
                'website': 'https://www.fortishealthcare.com/',
                'description': 'Multi-specialty hospital with mental health department'
            },
            {
                'id': 'delhi_mh_007',
                'name': 'Delhi Psychiatry Centre',
                'type': 'clinic',
                'address': 'B-13, Ground Floor, Lajpat Nagar 2, New Delhi, Delhi 110024',
                'phone': '+91-11-29831234',
                'services': ['Psychiatric consultation', 'Counseling', 'Therapy'],
                'specialties': ['Psychiatry', 'Clinical Psychology', 'Counseling'],
                'rating': 4.6,
                'coordinates': {'lat': 28.5788, 'lng': 77.2431},
                'website': 'https://delhipscentre.com/',
                'description': 'Private psychiatry and counseling center'
            },
            {
                'id': 'delhi_mh_008',
                'name': 'Mind Care Clinic',
                'type': 'clinic',
                'address': 'E-13, Defence Colony, New Delhi, Delhi 110024',
                'phone': '+91-11-24622121',
                'services': ['Mental health counseling', 'Psychotherapy', 'Stress management'],
                'specialties': ['Clinical Psychology', 'Counseling', 'Therapy'],
                'rating': 4.3,
                'coordinates': {'lat': 28.5744, 'lng': 77.2294},
                'website': 'https://mindcareclinic.com/',
                'description': 'Mental health clinic specializing in counseling and therapy'
            },
            {
                'id': 'delhi_mh_009',
                'name': 'AASRA Suicide Prevention Helpline',
                'type': 'helpline',
                'address': 'Mumbai, Maharashtra (Delhi Chapter)',
                'phone': '+91-9820466726',
                'services': ['Suicide prevention', 'Crisis counseling', '24/7 support'],
                'specialties': ['Crisis Intervention', 'Suicide Prevention'],
                'rating': 4.8,
                'coordinates': {'lat': 28.6139, 'lng': 77.2090},
                'website': 'https://www.aasra.info/',
                'description': '24/7 suicide prevention helpline with Delhi support'
            },
            {
                'id': 'delhi_mh_010',
                'name': 'Vandrevala Foundation',
                'type': 'support_group',
                'address': '92, Sunder Nagar, New Delhi, Delhi 110003',
                'phone': '+91-11-24362485',
                'services': ['Mental health support', 'Rehabilitation', 'Community programs'],
                'specialties': ['Mental Health', 'Rehabilitation', 'Community Support'],
                'rating': 4.5,
                'coordinates': {'lat': 28.6000, 'lng': 77.2000},
                'website': 'https://www.vandrevalafoundation.com/',
                'description': 'Mental health foundation providing support and rehabilitation services'
            }
        ]

    def _get_chennai_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Chennai"""
        return [
            {
                'id': 'chennai_mh_001',
                'name': 'Institute of Mental Health, Chennai',
                'type': 'hospital',
                'address': 'Kilpauk, Chennai, Tamil Nadu 600010',
                'phone': '+91-44-28361616',
                'services': ['Mental health treatment', 'Psychiatric care', 'Rehabilitation'],
                'specialties': ['Psychiatry', 'Psychology', 'Mental Health'],
                'rating': 4.2,
                'coordinates': {'lat': 13.0827, 'lng': 80.2707},
                'website': 'https://www.imhchen.com/',
                'description': 'Government mental health institute providing comprehensive psychiatric services'
            },
            {
                'id': 'chennai_mh_002',
                'name': 'Apollo Hospitals - Psychiatry Department',
                'type': 'hospital',
                'address': '21, Greams Lane, Off Greams Road, Chennai, Tamil Nadu 600006',
                'phone': '+91-44-28290200',
                'services': ['Mental health consultation', 'Psychiatric treatment', 'Counseling'],
                'specialties': ['Psychiatry', 'Mental Health', 'Psychology'],
                'rating': 4.4,
                'coordinates': {'lat': 13.0827, 'lng': 80.2707},
                'website': 'https://www.apollohospitals.com/',
                'description': 'Multi-specialty hospital with dedicated psychiatry department'
            },
            {
                'id': 'chennai_mh_003',
                'name': 'M.V. Hospital for Diabetes & Prof. M. Viswanathan Diabetes Research Centre',
                'type': 'hospital',
                'address': '4, West Mada Church Street, Royapuram, Chennai, Tamil Nadu 600013',
                'phone': '+91-44-25954132',
                'services': ['Mental health support', 'Diabetes-related mental health', 'Counseling'],
                'specialties': ['Mental Health', 'Diabetes Care', 'Psychology'],
                'rating': 4.1,
                'coordinates': {'lat': 13.1139, 'lng': 80.2917},
                'website': 'https://www.mvhospital.org/',
                'description': 'Specialized hospital with mental health support services'
            },
            {
                'id': 'chennai_mh_004',
                'name': 'Mind Zone Clinic',
                'type': 'clinic',
                'address': 'No. 12, 1st Floor, Khader Nawaz Khan Road, Nungambakkam, Chennai, Tamil Nadu 600006',
                'phone': '+91-44-28271414',
                'services': ['Psychiatric consultation', 'Counseling', 'Therapy'],
                'specialties': ['Psychiatry', 'Clinical Psychology', 'Counseling'],
                'rating': 4.5,
                'coordinates': {'lat': 13.0604, 'lng': 80.2496},
                'website': 'https://mindzoneclinic.com/',
                'description': 'Private mental health clinic specializing in psychiatry and counseling'
            },
            {
                'id': 'chennai_mh_005',
                'name': 'Sankara Nethralaya - Mental Health Support',
                'type': 'clinic',
                'address': '18, College Road, Nungambakkam, Chennai, Tamil Nadu 600006',
                'phone': '+91-44-28271616',
                'services': ['Mental health counseling', 'Stress management', 'Support services'],
                'specialties': ['Mental Health', 'Counseling', 'Psychology'],
                'rating': 4.3,
                'coordinates': {'lat': 13.0604, 'lng': 80.2496},
                'website': 'https://www.sankaranethralaya.org/',
                'description': 'Eye care hospital with mental health support services'
            },
            {
                'id': 'chennai_mh_006',
                'name': 'Tamil Nadu State Mental Health Authority',
                'type': 'helpline',
                'address': 'Chennai, Tamil Nadu',
                'phone': '1800-425-5555',
                'services': ['Mental health helpline', 'Crisis support', 'Information services'],
                'specialties': ['Mental Health Support', 'Crisis Intervention'],
                'rating': 4.0,
                'coordinates': {'lat': 13.0827, 'lng': 80.2707},
                'website': 'https://www.tnhealth.org/',
                'description': 'State mental health authority providing helpline services'
            },
            {
                'id': 'chennai_mh_007',
                'name': 'The Banyan - Chennai',
                'type': 'support_group',
                'address': 'No. 654, Anna Salai, Teynampet, Chennai, Tamil Nadu 600018',
                'phone': '+91-44-24327828',
                'services': ['Mental health support', 'Rehabilitation', 'Community programs'],
                'specialties': ['Mental Health', 'Rehabilitation', 'Community Support'],
                'rating': 4.4,
                'coordinates': {'lat': 13.0405, 'lng': 80.2337},
                'website': 'https://www.thebanyan.org/',
                'description': 'Mental health organization providing support and rehabilitation services'
            },
            {
                'id': 'chennai_mh_008',
                'name': 'SNEHA Suicide Prevention Centre - Chennai',
                'type': 'helpline',
                'address': 'Chennai, Tamil Nadu',
                'phone': '+91-44-24640050',
                'services': ['Suicide prevention', 'Crisis counseling', '24/7 support'],
                'specialties': ['Crisis Intervention', 'Suicide Prevention'],
                'rating': 4.6,
                'coordinates': {'lat': 13.0827, 'lng': 80.2707},
                'website': 'https://www.sneha.org.in/',
                'description': 'Suicide prevention center providing 24/7 crisis support'
            }
        ]

    def _get_mumbai_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Mumbai"""
        return [
            {
                'id': 'mumbai_mh_001',
                'name': 'KEM Hospital - Psychiatry Department',
                'type': 'hospital',
                'address': 'Parel, Mumbai, Maharashtra 400012',
                'phone': '+91-22-24136051',
                'services': ['Mental health treatment', 'Psychiatric care', 'Emergency services'],
                'specialties': ['Psychiatry', 'Mental Health', 'Psychology'],
                'rating': 4.3,
                'coordinates': {'lat': 19.0760, 'lng': 72.8777},
                'website': 'https://www.kem.edu/',
                'description': 'Government medical college hospital with psychiatry department'
            },
            {
                'id': 'mumbai_mh_002',
                'name': 'Lilavati Hospital - Mental Health Unit',
                'type': 'hospital',
                'address': 'A-791, Bandra Reclamation, Bandra West, Mumbai, Maharashtra 400050',
                'phone': '+91-22-26751000',
                'services': ['Mental health consultation', 'Psychiatric treatment'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 4.2,
                'coordinates': {'lat': 19.0544, 'lng': 72.8406},
                'website': 'https://www.lilavatihospital.com/',
                'description': 'Multi-specialty hospital with mental health services'
            },
            {
                'id': 'mumbai_mh_003',
                'name': 'AASRA Suicide Prevention Helpline',
                'type': 'helpline',
                'address': 'Mumbai, Maharashtra',
                'phone': '+91-9820466726',
                'services': ['Suicide prevention', 'Crisis counseling', '24/7 support'],
                'specialties': ['Crisis Intervention', 'Suicide Prevention'],
                'rating': 4.8,
                'coordinates': {'lat': 19.0760, 'lng': 72.8777},
                'website': 'https://www.aasra.info/',
                'description': '24/7 suicide prevention helpline'
            }
        ]

    def _get_bangalore_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Bangalore"""
        return [
            {
                'id': 'bangalore_mh_001',
                'name': 'National Institute of Mental Health and Neurosciences (NIMHANS)',
                'type': 'hospital',
                'address': 'Hosur Road, Bangalore, Karnataka 560029',
                'phone': '+91-80-26995000',
                'services': ['Mental health treatment', 'Psychiatric care', 'Research'],
                'specialties': ['Psychiatry', 'Neurology', 'Psychology'],
                'rating': 4.5,
                'coordinates': {'lat': 12.9432, 'lng': 77.5963},
                'website': 'https://www.nimhans.ac.in/',
                'description': 'Premier mental health and neuroscience institute'
            },
            {
                'id': 'bangalore_mh_002',
                'name': 'Manipal Hospital - Psychiatry Department',
                'type': 'hospital',
                'address': '98, HAL Airport Road, Bangalore, Karnataka 560017',
                'phone': '+91-80-25024444',
                'services': ['Mental health consultation', 'Psychiatric treatment'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 4.3,
                'coordinates': {'lat': 12.9592, 'lng': 77.6974},
                'website': 'https://www.manipalhospitals.com/',
                'description': 'Multi-specialty hospital with psychiatry department'
            }
        ]

    def _get_kolkata_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Kolkata"""
        return [
            {
                'id': 'kolkata_mh_001',
                'name': 'Institute of Psychiatry - Kolkata',
                'type': 'hospital',
                'address': '7, D.L. Khan Road, Kolkata, West Bengal 700025',
                'phone': '+91-33-22351223',
                'services': ['Mental health treatment', 'Psychiatric care', 'Rehabilitation'],
                'specialties': ['Psychiatry', 'Psychology', 'Mental Health'],
                'rating': 4.2,
                'coordinates': {'lat': 22.5726, 'lng': 88.3639},
                'website': 'https://www.ipkcalcutta.org/',
                'description': 'Specialized psychiatric institute'
            }
        ]

    def _get_pune_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Pune"""
        return [
            {
                'id': 'pune_mh_001',
                'name': 'Ruby Hall Clinic - Mental Health Department',
                'type': 'hospital',
                'address': '40, Sassoon Road, Pune, Maharashtra 411001',
                'phone': '+91-20-26163391',
                'services': ['Mental health consultation', 'Psychiatric treatment'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 4.1,
                'coordinates': {'lat': 18.5308, 'lng': 73.8475},
                'website': 'https://www.rubyhall.com/',
                'description': 'Multi-specialty hospital with mental health services'
            }
        ]

    def _get_hyderabad_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Hyderabad"""
        return [
            {
                'id': 'hyderabad_mh_001',
                'name': 'Institute of Mental Health, Hyderabad',
                'type': 'hospital',
                'address': 'Erragadda, Hyderabad, Telangana 500038',
                'phone': '+91-40-23814444',
                'services': ['Mental health treatment', 'Psychiatric care'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 4.0,
                'coordinates': {'lat': 17.3850, 'lng': 78.4867},
                'website': 'https://www.imhhyd.org/',
                'description': 'Government mental health institute'
            }
        ]

    def _get_ahmedabad_mental_health_services(self) -> List[Dict[str, Any]]:
        """Get known mental health services in Ahmedabad"""
        return [
            {
                'id': 'ahmedabad_mh_001',
                'name': 'BJ Medical College - Psychiatry Department',
                'type': 'hospital',
                'address': 'Asarwa, Ahmedabad, Gujarat 380016',
                'phone': '+91-79-22680074',
                'services': ['Mental health treatment', 'Psychiatric care'],
                'specialties': ['Psychiatry', 'Mental Health'],
                'rating': 3.9,
                'coordinates': {'lat': 23.0225, 'lng': 72.5714},
                'website': 'https://www.bjmc.org/',
                'description': 'Medical college with psychiatry department'
            }
        ]

    def _search_google_places(self, location: str, service_type: str) -> List[Dict[str, Any]]:
        """Search Google Places API for mental health services"""
        if not self.google_api_key:
            return []

        try:
            # Search for mental health related places
            query = f"mental health {service_type} in {location}"
            url = f"https://maps.googleapis.com/maps/api/place/textsearch/json"

            params = {
                'query': query,
                'key': self.google_api_key,
                'type': 'health'
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            results = []
            if data.get('results'):
                for place in data['results'][:5]:  # Limit to 5 results
                    results.append({
                        'id': place.get('place_id', ''),
                        'name': place.get('name', ''),
                        'type': 'facility',
                        'address': place.get('formatted_address', ''),
                        'rating': place.get('rating', 0),
                        'coordinates': {
                            'lat': place.get('geometry', {}).get('location', {}).get('lat', 0),
                            'lng': place.get('geometry', {}).get('location', {}).get('lng', 0)
                        },
                        'services': ['Mental health services'],
                        'specialties': ['Mental Health'],
                        'description': f"Mental health facility in {location}"
                    })

            return results

        except Exception as e:
            current_app.logger.error(f"Google Places API error: {str(e)}")
            return []

    def get_service_types(self) -> List[str]:
        """Get available service types"""
        return [
            'all',
            'hospital',
            'clinic',
            'therapist',
            'support_group',
            'helpline',
            'rehabilitation'
        ]

    def get_supported_locations(self) -> List[str]:
        """Get supported locations"""
        return [
            'Delhi',
            'New Delhi',
            'Delhi NCR',
            'Mumbai',
            'Bangalore',
            'Chennai',
            'Kolkata',
            'Pune',
            'Hyderabad',
            'Ahmedabad'
        ]
