import React, { useEffect, useState } from "react";
import "./style.css";

function App() {
  const [items, setItems] = useState([]);
  const [platform, setPlatform] = useState("");
  const [downloadLink, setDownloadLink] = useState("");

  const API_URL = "http://localhost:5000/api/data";

  const fetchItems = async () => {
    const response = await fetch(API_URL);
    const data = await response.json();
    setItems(data);
  };

  useEffect(() => {
    fetchItems();
  }, []);

  const addItem = async () => {
    if (!platform || !downloadLink) return;

    await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        platform: platform,
        download_link: downloadLink,
      }),
    });

    setPlatform("");
    setDownloadLink("");

    fetchItems();
  };

  const deleteItem = async (id) => {
    await fetch(`${API_URL}/${id}`, {
      method: "DELETE",
    });

    fetchItems();
  };

  return (
    <div className="container">
      <h1>Best app in your life</h1>

      <p className="subtitle">
        Download and use super-app in all platforms
      </p>

      <div className="form">
        <input
          type="text"
          placeholder="Platform"
          value={platform}
          onChange={(e) => setPlatform(e.target.value)}
        />

        <input
          type="text"
          placeholder="Download Link"
          value={downloadLink}
          onChange={(e) => setDownloadLink(e.target.value)}
        />

        <button className="btn" onClick={addItem}>
          Add Platform
        </button>
      </div>

      <div className="cards">
        {items.map((item) => (
          <div className="card" key={item.id}>
            <h2>{item.platform}</h2>

            <p>Download application for {item.platform}</p>

            <a
              href={item.download_link}
              target="_blank"
              rel="noreferrer"
              className="btn"
            >
              Download
            </a>

            <button
              className="delete-btn"
              onClick={() => deleteItem(item.id)}
            >
              Delete
            </button>
          </div>
        ))}
      </div>

      <footer>
        © 2025 SuperApp of Amantur and Ulan
      </footer>
    </div>
  );
}

export default App;
