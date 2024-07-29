import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const ClassDetail = () => {
    const { id } = useParams();
    const [classDetail, setClassDetail] = useState(null);
    const [rating, setRating] = useState('');
    const [comments, setComments] = useState([]);
    const [comment, setComment] = useState('');
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchClassDetails = async () => {
            try {
                const response = await axios.get(`/class/${id}`);
                setClassDetail(response.data);
            } catch (error) {
                console.error('Error fetching class details:', error);
                setError('Error fetching class details');
            }
        };

        const fetchComments = async () => {
            try {
                const response = await axios.get(`/comments?class_id=${id}`);
                setComments(response.data);
            } catch (error) {
                console.error('Error fetching comments:', error);
                setError('Error fetching comments');
            }
        };

        fetchClassDetails();
        fetchComments();
    }, [id]);

    const handleRatingSubmit = async () => {
        if (rating < 1 || rating > 5) {
            setError('Rating must be between 1 and 5');
            return;
        }

        try {
            const response = await axios.post('/rate', { stars: rating, class_id: id });
            console.log('Rating submitted:', response.data);
        } catch (error) {
            console.error('Error submitting rating:', error);
            setError('Error submitting rating');
        }
    };

    const handleCommentSubmit = async () => {
        try {
            const response = await axios.post('/comments', { content: comment, class_id: id });
            setComments([...comments, response.data]);
            setComment('');
            setComments([...comments, { content: comment, user: 'You' }]);
            setComment('');
        } catch (error) {
            console.error('Error submitting comment:', error);
            setError('Error submitting comment');
        }
    };

    return (
        <div>
            {error && <div className="error">{error}</div>}
            {classDetail && (
                <div>
                    <h1>{classDetail.name}</h1>
                    <div>
                        <h2>Ratings</h2>
                        <input
                            type="number"
                            value={rating}
                            onChange={e => setRating(e.target.value)}
                            max="5"
                            min="1"
                        />
                        <button onClick={handleRatingSubmit}>Submit Rating</button>
                    </div>
                    <div>
                        <h2>Comments</h2>
                        <ul>
                            {comments.map((comment, index) => (
                                <li key={index}>{comment.user}: {comment.content}</li>
                            ))}
                        </ul>
                        <textarea
                            value={comment}
                            onChange={e => setComment(e.target.value)}
                        />
                        <button onClick={handleCommentSubmit}>Submit Comment</button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ClassDetail;
