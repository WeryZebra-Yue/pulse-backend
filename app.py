from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from auth.jwt_bearer import JWTBearer
from config.config import initiate_database
from routes.home import router as home_router
from routes.alert import router as alert_router
from routes.charity import router as charity_router
from routes.user import router as user_router
from routes.donation import router as donation_router
from routes.form import router as form_router
from routes.alert_chat import router as alert_chat_router

app = FastAPI(
    title="AidAgent API",
    description="""
    **AidAgent** is a comprehensive blockchain-based humanitarian aid coordination platform that connects emergency alerts, charitable organizations, and cryptocurrency donations.

    ## 🚨 Emergency Management
    * **Alerts**: Create, manage, and track emergency alerts with real-time updates
    * **Location-based filtering**: Find alerts relevant to specific geographical areas
    * **Staleness detection**: Automatic data freshness management for accurate information

    ## 🏢 Charity Management  
    * **Organization registry**: Comprehensive database of verified charitable organizations
    * **Emergency response**: Link charities to specific alerts for targeted aid coordination
    * **Due diligence**: Detailed charity profiles with contact information and verification data

    ## 💰 Cryptocurrency Donations
    * **Multi-currency support**: Accept donations in ETH, BTC, USDC, and other cryptocurrencies
    * **Wallet-based identity**: Secure blockchain-based donor identification
    * **Transparent tracking**: Complete audit trails for all donation transactions

    ## 👥 User Management
    * **Wallet integration**: User accounts linked to blockchain wallet addresses  
    * **Location services**: Optional GPS-based user positioning for relevant alerts
    * **Profile management**: Comprehensive user data with privacy controls

    ## 💬 Communication Forms
    * **Emergency coordination**: Real-time messaging for crisis response teams
    * **Stakeholder updates**: Chronological communication threads per emergency
    * **Audit trails**: Complete message history with timestamps and user attribution

    ## 🔐 Security Features
    * **JWT Authentication**: Secure API access with bearer token validation
    * **MongoDB Integration**: Scalable document-based data storage with Beanie ODM
    * **Data Integrity**: Comprehensive validation and error handling

    This API enables seamless coordination between emergency responders, charitable organizations, and donors through blockchain technology and real-time communication systems.
    """,
    version="1.0.0",
    contact={
        "name": "AidAgent Development Team",
        "email": "api@aidagent.com",
        "url": "https://aidagent.com/contact"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    },
    terms_of_service="https://aidagent.com/terms",
    openapi_tags=[
        {
            "name": "Root",
            "description": "Welcome page and API navigation with modern responsive design"
        },
        {
            "name": "Users",
            "description": "User account management with wallet-based identity and location services"
        },
        {
            "name": "Alerts", 
            "description": "Emergency alert creation, management, and real-time updates with location filtering"
        },
        {
            "name": "Charities",
            "description": "Charitable organization registry, verification, and emergency response coordination"
        },
        {
            "name": "Donations",
            "description": "Cryptocurrency donation tracking, transparency, and multi-currency transaction management"
        },
        {
            "name": "Forms",
            "description": "Emergency communication systems with real-time messaging and audit trails"
        }
    ]
)
app.add_middleware(
    # CORS middleware to allow cross-origin requests
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add CORS middleware
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:5173",
#         "http://127.0.0.1:5173",
#         "https://localhost:5173",
#         "https://127.0.0.1:5173",
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

token_listener = JWTBearer()


@app.on_event("startup")
async def start_database():
    await initiate_database()


# Include routers
app.include_router(home_router, tags=["Root"])
app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(alert_router, prefix="/alerts", tags=["Alerts"])
app.include_router(charity_router, prefix="/charities", tags=["Charities"])
app.include_router(donation_router, prefix="/donations", tags=["Donations"])
app.include_router(form_router, prefix="/forms", tags=["Forms"])
app.include_router(alert_chat_router, prefix="/alerts/chat", tags=["Alert Chat"])