import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE = "http://localhost:8000"; // Replace with your FastAPI backend URL

function UrlShortner(){
    const [originalUrl, setOriginalUrl] = useState("");
    const [urls, setUrls] =useState([]);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    
}