from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from Back.models import FeedbackCreate
from Back.auth import get_current_user
from Back.db import feedback_collection

router = APIRouter()

@router.post("/feedback", response_model=dict, status_code=status.HTTP_201_CREATED)
async def create_feedback(feedback_data: FeedbackCreate,current_user: dict = Depends(get_current_user)
                          ):
    try:
        # Check if the user is authenticated
        if current_user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

        
        # Store feedback in the database
        feedback = {
            "user_email": current_user["email"],
            "feedback_text": feedback_data.feedback_text,
            "rating": feedback_data.rating,
            
        }
        result =  feedback_collection.insert_one(feedback)
        if result:
            return {"message": "Feedback submitted successfully"}
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to store feedback")

    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )


@router.get("/feedback", response_model=list)
async def get_feedback(current_user: dict = Depends(get_current_user)):
    try:
        # Check if the user is authenticated and has the admin role
        if current_user is None :
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
        # Fetch feedback from the database
        feedback_list =list(feedback_collection.find())
        for feedback in feedback_list:
            feedback['_id'] = str(feedback['_id'])
        return feedback_list

    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal Server Error: {str(e)}"
        )