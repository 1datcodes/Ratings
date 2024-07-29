import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ClassList = () => {
    const [classes, setClasses] = useState([]);

    useEffect(() => {
        axios.get('/classes')
            .then(response => setClasses(response.data))
            .catch(error => console.error('Error fetching classes:', error));
    }, []);

    return (
        <div>
            <h1>Classes</h1>
            <ul>
                {classes.map(cls => (
                    <li key={cls.id}>
                        <a href={`/class/${cls.id}`}>{cls.name}</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ClassList;
