import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_pagination(current_request, selection):
    page = current_request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_objects = [obj.format() for obj in selection]

    return formatted_objects[start:end]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    # resources = {r'*/api/*': {'origins': '*'}}
    CORS(app)

    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if request.method == 'OPTIONS':
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
            response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
            response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)
        else:
            response.headers.add('Access-Control-Allow-Credentials', 'true')
            if origin:
                response.headers.add('Access-Control-Allow-Origin', origin)

        return response

    '''
    @TODO: Create an endpoint to handle GET requests for all available categories.
    '''

    @app.route("/categories", methods=["GET"])
    def get_categories():
        categories = Category.query.all()
        # abort 404 if no categories found
        if len(categories) == 0:
            abort(404)

        all_categories = {}
        for cat in categories:
            all_categories[cat.id] = cat.type

        return jsonify({
            'success': True,
            'categories': all_categories
        })

    '''
    @TODO: 
    Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). 
    This endpoint should return a list of questions, number of total questions, current category, categories. 
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions. 
    '''

    # return data to view
    @app.route('/questions', methods=["GET"])
    def index():
        # all questions
        questions = Question.query.order_by(Question.id).all()
        # paginate questions
        current_questions = create_pagination(request, questions)
        #  if no questions abort 404
        if len(current_questions) == 0:
            abort(404)

        # all categories
        categories = Category.query.order_by(Category.id).all()
        all_categories = {}
        for cat in categories:
            all_categories[cat.id] = cat.type

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(questions),
            'current_category': False,
            'categories': all_categories
        })

    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
    
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            # Delete Targeted question
            question = Question.query.get(question_id)

            if question is None:
                abort(400)

            question.delete()

            return jsonify({'success': True, 'message': f'deleted {question.id}'})

        except Exception as e:
            return jsonify({'status': 'error',
                            'message': f'Question with id: {question_id} not deleted successfully',
                            'error': str(e)})

    '''
    @TODO: 
    Create an endpoint to POST a new question, which will require the question and answer text, 
    category, and difficulty score.
    
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''
    # @app.route("/questions", methods=["POST"])
    # def create_search():
    #     body = request.get_json()
    #
    #     try:
    #         new_question = Question(**body)
    #         Question.insert(new_question)
    #
    #         return jsonify({
    #             'success': True,
    #             'message': f'Question created with ID:{Question.id}',
    #         })
    #
    #     except Exception as e:
    #         abort(422)

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
    
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    @app.route("/questions", methods=['POST', 'OPTIONS'])
    def create_or_search():
        body = request.get_json()
        search_term = ''
        if 'searchTerm' in body and body['searchTerm'] != '':
            # search request
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            all_questions = create_pagination(request, questions)
            # all categories
            categories = Category.query.order_by(Category.id).all()
            all_categories = {}
            for cat in categories:
                all_categories[cat.id] = cat.type

            return jsonify({
                'success': True,
                'questions': all_questions,
                'total_questions': len(questions),
                'current_category': False,
                'categories': all_categories
            })
        else:
            try:
                new_question = Question(**body)
                Question.insert(new_question)

                return jsonify({
                    'success': True,
                    'message': f'Question created with ID:{Question.id}',
                })

            except Exception as e:
                abort(422)

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
    
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
    
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'status': 'error',
                        'message': f'{error}',
                        'error': 400}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'status': 'error',
                        'message': f'{error}',
                        'error': 404}), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({'status': 'error',
                        'message': f'{error}',
                        'error': 422}), 422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'status': 'error',
                        'message': f'{error}',
                        'error': 405}), 405

    return app

    return app
