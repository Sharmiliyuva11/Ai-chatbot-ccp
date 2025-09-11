from pymongo import MongoClient
from bson import ObjectId
import os
import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB setup
try:
    mongo_uri = os.getenv("MONGO_URI")
    if mongo_uri and mongo_uri != "mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority":
        try:
            client = MongoClient(
                mongo_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            client.admin.command('ping')
            db = client.get_database("ai_chatbot_ccp")
            projects_collection = db["coding_projects"]
            templates_collection = db["coding_templates"]
            snippets_collection = db["coding_snippets"]
            print("✅ Connected to MongoDB successfully with SSL for coding collections")
        except Exception as ssl_error:
            print(f"⚠️ SSL connection failed: {ssl_error}")
            print("⚠️ Trying without SSL...")
            client = MongoClient(
                mongo_uri,
                tls=False,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            client.admin.command('ping')
            db = client.get_database("ai_chatbot_ccp")
            projects_collection = db["coding_projects"]
            templates_collection = db["coding_templates"]
            snippets_collection = db["coding_snippets"]
            print("✅ Connected to MongoDB successfully without SSL for coding collections")
    else:
        print("⚠️ Warning: Using in-memory storage for coding collections. Set MONGO_URI in .env for persistent storage.")
        projects_collection = None
        templates_collection = None
        snippets_collection = None
except Exception as e:
    print(f"❌ MongoDB connection failed: {e}")
    print("⚠️ Using in-memory storage for coding collections.")
    projects_collection = None
    templates_collection = None
    snippets_collection = None

# In-memory storage for testing
_projects_memory = []
_templates_memory = []
_snippets_memory = []

class CodingProject:
    @staticmethod
    def get_all_projects():
        """Get all projects"""
        if projects_collection is not None:
            return list(projects_collection.find({}))
        else:
            return _projects_memory.copy()

    @staticmethod
    def get_projects_by_user(user_id):
        """Get projects by user"""
        if projects_collection is not None:
            return list(projects_collection.find({"user_id": user_id}))
        else:
            return [p for p in _projects_memory if p.get('user_id') == user_id]

    @staticmethod
    def find_by_id(project_id):
        """Find project by ID"""
        if projects_collection is not None:
            try:
                return projects_collection.find_one({"_id": ObjectId(project_id)})
            except:
                return None
        else:
            for project in _projects_memory:
                if str(project.get('_id')) == str(project_id):
                    return project
            return None

    @staticmethod
    def create_project(project_data):
        """Create a new project"""
        project_data['created_at'] = datetime.datetime.utcnow()
        project_data['updated_at'] = datetime.datetime.utcnow()

        if projects_collection is not None:
            result = projects_collection.insert_one(project_data)
            project_data['_id'] = result.inserted_id
            return project_data
        else:
            project_id = len(_projects_memory) + 1
            project_data['_id'] = project_id
            _projects_memory.append(project_data)
            return project_data

    @staticmethod
    def update_project(project_id, update_data):
        """Update project data"""
        update_data['updated_at'] = datetime.datetime.utcnow()

        if projects_collection is not None:
            try:
                result = projects_collection.update_one(
                    {"_id": ObjectId(project_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            except:
                return False
        else:
            for i, project in enumerate(_projects_memory):
                if str(project.get('_id')) == str(project_id):
                    _projects_memory[i].update(update_data)
                    return True
            return False

    @staticmethod
    def delete_project(project_id, user_id):
        """Delete project (only by owner)"""
        if projects_collection is not None:
            try:
                result = projects_collection.delete_one({
                    "_id": ObjectId(project_id),
                    "user_id": user_id
                })
                return result.deleted_count > 0
            except:
                return False
        else:
            for i, project in enumerate(_projects_memory):
                if str(project.get('_id')) == str(project_id) and project.get('user_id') == user_id:
                    del _projects_memory[i]
                    return True
            return False

class CodingTemplate:
    @staticmethod
    def get_all_templates():
        """Get all templates"""
        if templates_collection is not None:
            return list(templates_collection.find({}))
        else:
            return _templates_memory.copy()

    @staticmethod
    def get_templates_by_user(user_id):
        """Get templates by user"""
        if templates_collection is not None:
            return list(templates_collection.find({"user_id": user_id}))
        else:
            return [t for t in _templates_memory if t.get('user_id') == user_id]

    @staticmethod
    def find_by_id(template_id):
        """Find template by ID"""
        if templates_collection is not None:
            try:
                return templates_collection.find_one({"_id": ObjectId(template_id)})
            except:
                return None
        else:
            for template in _templates_memory:
                if str(template.get('_id')) == str(template_id):
                    return template
            return None

    @staticmethod
    def create_template(template_data):
        """Create a new template"""
        template_data['created_at'] = datetime.datetime.utcnow()
        template_data['updated_at'] = datetime.datetime.utcnow()

        if templates_collection is not None:
            result = templates_collection.insert_one(template_data)
            template_data['_id'] = result.inserted_id
            return template_data
        else:
            template_id = len(_templates_memory) + 1
            template_data['_id'] = template_id
            _templates_memory.append(template_data)
            return template_data

    @staticmethod
    def update_template(template_id, update_data):
        """Update template data"""
        update_data['updated_at'] = datetime.datetime.utcnow()

        if templates_collection is not None:
            try:
                result = templates_collection.update_one(
                    {"_id": ObjectId(template_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            except:
                return False
        else:
            for i, template in enumerate(_templates_memory):
                if str(template.get('_id')) == str(template_id):
                    _templates_memory[i].update(update_data)
                    return True
            return False

    @staticmethod
    def delete_template(template_id, user_id):
        """Delete template (only by owner)"""
        if templates_collection is not None:
            try:
                result = templates_collection.delete_one({
                    "_id": ObjectId(template_id),
                    "user_id": user_id
                })
                return result.deleted_count > 0
            except:
                return False
        else:
            for i, template in enumerate(_templates_memory):
                if str(template.get('_id')) == str(template_id) and template.get('user_id') == user_id:
                    del _templates_memory[i]
                    return True
            return False

class CodeSnippet:
    @staticmethod
    def get_all_snippets():
        """Get all snippets"""
        if snippets_collection is not None:
            return list(snippets_collection.find({}))
        else:
            return _snippets_memory.copy()

    @staticmethod
    def get_snippets_by_user(user_id):
        """Get snippets by user"""
        if snippets_collection is not None:
            return list(snippets_collection.find({"user_id": user_id}))
        else:
            return [s for s in _snippets_memory if s.get('user_id') == user_id]

    @staticmethod
    def find_by_id(snippet_id):
        """Find snippet by ID"""
        if snippets_collection is not None:
            try:
                return snippets_collection.find_one({"_id": ObjectId(snippet_id)})
            except:
                return None
        else:
            for snippet in _snippets_memory:
                if str(snippet.get('_id')) == str(snippet_id):
                    return snippet
            return None

    @staticmethod
    def create_snippet(snippet_data):
        """Create a new snippet"""
        snippet_data['created_at'] = datetime.datetime.utcnow()
        snippet_data['updated_at'] = datetime.datetime.utcnow()

        if snippets_collection is not None:
            result = snippets_collection.insert_one(snippet_data)
            snippet_data['_id'] = result.inserted_id
            return snippet_data
        else:
            snippet_id = len(_snippets_memory) + 1
            snippet_data['_id'] = snippet_id
            _snippets_memory.append(snippet_data)
            return snippet_data

    @staticmethod
    def update_snippet(snippet_id, update_data):
        """Update snippet data"""
        update_data['updated_at'] = datetime.datetime.utcnow()

        if snippets_collection is not None:
            try:
                result = snippets_collection.update_one(
                    {"_id": ObjectId(snippet_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            except:
                return False
        else:
            for i, snippet in enumerate(_snippets_memory):
                if str(snippet.get('_id')) == str(snippet_id):
                    _snippets_memory[i].update(update_data)
                    return True
            return False

    @staticmethod
    def delete_snippet(snippet_id, user_id):
        """Delete snippet (only by owner)"""
        if snippets_collection is not None:
            try:
                result = snippets_collection.delete_one({
                    "_id": ObjectId(snippet_id),
                    "user_id": user_id
                })
                return result.deleted_count > 0
            except:
                return False
        else:
            for i, snippet in enumerate(_snippets_memory):
                if str(snippet.get('_id')) == str(snippet_id) and snippet.get('user_id') == user_id:
                    del _snippets_memory[i]
                    return True
            return False
