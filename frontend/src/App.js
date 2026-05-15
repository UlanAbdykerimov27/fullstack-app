import React, { useEffect, useState } from "react";

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
    <div style={{ padding: "30px", fontFamily: "Arial" }}>
      <h1>Super App Downloads</h1>

      <h3>Student: Ulan Abdykerimov</h3>
      <h3>ID: YOUR_ID</h3>

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

      <button onClick={addItem}>Add</button>

      <hr />

      {items.map((item) => (
        <div key={item.id}>
          <h3>{item.platform}</h3>

          <a href={item.download_link}>
            {item.download_link}
          </a>

          <br />

          <button onClick={() => deleteItem(item.id)}>
            Delete
          </button>

          <hr />
        </div>
      ))}
    </div>
  );
}

export default App;
