"""
Chat Routes for Deed Reader Pro
------------------------------
Handles interactive Q&A about deed documents using Claude.
"""

import logging
from flask import Blueprint, request, jsonify, session
from services.claude_service import ClaudeService

logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

# In-memory storage for chat sessions (in production, use Redis or database)
chat_sessions = {}

@chat_bp.route('/ask', methods=['POST'])
def ask_question():
    """Ask a question about the deed document."""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data or 'document_text' not in data:
            return jsonify({'error': 'Question and document text are required'}), 400
        
        question = data['question']
        document_text = data['document_text']
        session_id = data.get('session_id', 'default')
        
        if not question.strip():
            return jsonify({'error': 'Question cannot be empty'}), 400
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI chat not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Get chat history for this session
        chat_history = chat_sessions.get(session_id, [])
        
        # Get answer from Claude
        answer = ClaudeService.answer_question(
            document_text=document_text,
            question=question,
            chat_history=chat_history
        )
        
        # Store this exchange in chat history
        exchange = {
            'question': question,
            'answer': answer,
            'timestamp': None  # Could add timestamp
        }
        
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []
        
        chat_sessions[session_id].append(exchange)
        
        # Keep only last 20 exchanges to manage memory
        if len(chat_sessions[session_id]) > 20:
            chat_sessions[session_id] = chat_sessions[session_id][-20:]
        
        return jsonify({
            'success': True,
            'question': question,
            'answer': answer,
            'session_id': session_id,
            'exchange_count': len(chat_sessions[session_id]),
            'message': 'Question answered successfully'
        })
        
    except Exception as e:
        logger.error(f"Error answering question: {e}")
        return jsonify({
            'error': 'Failed to answer question',
            'message': str(e)
        }), 500

@chat_bp.route('/history/<session_id>', methods=['GET'])
def get_chat_history(session_id):
    """Get chat history for a session."""
    try:
        history = chat_sessions.get(session_id, [])
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'history': history,
            'exchange_count': len(history),
            'message': 'Chat history retrieved successfully'
        })
        
    except Exception as e:
        logger.error(f"Error retrieving chat history: {e}")
        return jsonify({
            'error': 'Failed to retrieve chat history',
            'message': str(e)
        }), 500

@chat_bp.route('/clear/<session_id>', methods=['DELETE'])
def clear_chat_history(session_id):
    """Clear chat history for a session."""
    try:
        if session_id in chat_sessions:
            del chat_sessions[session_id]
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': 'Chat history cleared successfully'
        })
        
    except Exception as e:
        logger.error(f"Error clearing chat history: {e}")
        return jsonify({
            'error': 'Failed to clear chat history',
            'message': str(e)
        }), 500

@chat_bp.route('/sessions', methods=['GET'])
def list_chat_sessions():
    """List all active chat sessions."""
    try:
        sessions = [
            {
                'session_id': session_id,
                'exchange_count': len(history),
                'last_activity': history[-1].get('timestamp') if history else None
            }
            for session_id, history in chat_sessions.items()
        ]
        
        return jsonify({
            'success': True,
            'sessions': sessions,
            'total_sessions': len(sessions),
            'message': 'Chat sessions listed successfully'
        })
        
    except Exception as e:
        logger.error(f"Error listing chat sessions: {e}")
        return jsonify({
            'error': 'Failed to list chat sessions',
            'message': str(e)
        }), 500

@chat_bp.route('/suggestions', methods=['POST'])
def get_question_suggestions():
    """Get suggested questions based on the document content."""
    try:
        data = request.get_json()
        
        if not data or 'document_text' not in data:
            return jsonify({'error': 'Document text is required'}), 400
        
        document_text = data['document_text']
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI suggestions not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Generate suggested questions using Claude
        suggestions_prompt = f"""
        Based on this deed document, suggest 5-7 relevant questions that a surveyor or property owner might want to ask. 
        Focus on practical questions about boundaries, measurements, monuments, and legal descriptions.
        
        Document excerpt:
        {document_text[:2000]}...
        
        Return a simple list of questions, one per line:
        """
        
        try:
            message = ClaudeService._client.messages.create(
                model=ClaudeService._model,
                messages=[{"role": "user", "content": suggestions_prompt}],
                max_tokens=500,
                temperature=0.5,
                system="You are a helpful assistant suggesting relevant questions about deed documents for surveyors."
            )
            
            suggestions_text = message.content[0].text.strip()
            
            # Parse suggestions into a list
            suggestions = [
                line.strip().lstrip('- ').lstrip('• ').lstrip('* ')
                for line in suggestions_text.split('\n')
                if line.strip() and '?' in line
            ]
            
            # Fallback suggestions if none generated
            if not suggestions:
                suggestions = [
                    "What are the main boundary measurements?",
                    "Who are the grantor and grantee?",
                    "What monuments are referenced in this deed?",
                    "What is the total acreage of the property?",
                    "Are there any easements or restrictions mentioned?"
                ]
            
            return jsonify({
                'success': True,
                'suggestions': suggestions[:7],  # Limit to 7 suggestions
                'message': 'Question suggestions generated successfully'
            })
            
        except Exception as e:
            logger.error(f"Error generating suggestions with Claude: {e}")
            
            # Fallback suggestions
            fallback_suggestions = [
                "What are the boundary measurements for this property?",
                "Who is transferring ownership in this deed?",
                "What monuments or markers are mentioned?",
                "What is the legal description of the property?",
                "Are there any recorded deed references?",
                "What is the total area or acreage?",
                "Are there any special conditions or restrictions?"
            ]
            
            return jsonify({
                'success': True,
                'suggestions': fallback_suggestions,
                'message': 'Fallback question suggestions provided'
            })
        
    except Exception as e:
        logger.error(f"Error getting question suggestions: {e}")
        return jsonify({
            'error': 'Failed to get question suggestions',
            'message': str(e)
        }), 500

@chat_bp.route('/explain', methods=['POST'])
def explain_term():
    """Explain a specific surveying or legal term found in the deed."""
    try:
        data = request.get_json()
        
        if not data or 'term' not in data:
            return jsonify({'error': 'Term is required'}), 400
        
        term = data['term']
        context = data.get('document_text', '')
        
        if not term.strip():
            return jsonify({'error': 'Term cannot be empty'}), 400
        
        # Check if Claude is available
        if not ClaudeService.is_available():
            return jsonify({
                'error': 'AI explanation not available',
                'message': 'Claude service is not configured'
            }), 503
        
        # Generate explanation using Claude
        explanation_prompt = f"""
        Explain the following surveying or legal term in the context of deed documents.
        Provide a clear, concise explanation that would be helpful for surveyors or property owners.
        
        Term: "{term}"
        
        Context from deed:
        {context[:1000] if context else 'No additional context provided'}
        
        Provide a practical explanation focusing on how this term is used in surveying and deed interpretation.
        """
        
        try:
            message = ClaudeService._client.messages.create(
                model=ClaudeService._model,
                messages=[{"role": "user", "content": explanation_prompt}],
                max_tokens=300,
                temperature=0.3,
                system="You are an expert surveyor and legal assistant explaining technical terms clearly and accurately."
            )
            
            explanation = message.content[0].text.strip()
            
            return jsonify({
                'success': True,
                'term': term,
                'explanation': explanation,
                'message': 'Term explanation generated successfully'
            })
            
        except Exception as e:
            logger.error(f"Error generating explanation with Claude: {e}")
            return jsonify({
                'error': 'Failed to generate explanation',
                'message': str(e)
            }), 500
        
    except Exception as e:
        logger.error(f"Error explaining term: {e}")
        return jsonify({
            'error': 'Failed to explain term',
            'message': str(e)
        }), 500 