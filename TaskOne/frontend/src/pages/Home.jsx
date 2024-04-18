import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import api from "../api";
import "../styles/Home.css";
import Navbar from "../components/Navbar";

function Home() {
  const [videoList, setVideoList] = useState([]);
  const [isSearched, setIsSearched] = useState(false);
  const [searchQuery, setSearchQuery] = useState(null);
  const [searchVideoList, setSearchVideoList] = useState([]);

  const onSearchHandler = (event) => {
    if (event.target.value == "") {
      setIsSearched(false);
      return;
    }
    setIsSearched(true);
    setSearchQuery(event.target.value);
    api
      .get(`api/videos/search/${event.target.value}/`)
      .then((response) => {
        setSearchVideoList(() => {
          return response.data;
        });
      })
      .catch((error) => {
        console.log(error);
      });
  };
  useEffect(() => {
    api.get("api/videos/").then((response) => {
      setVideoList(response.data);
    });
  }, []);
  return (
    <>
      <Navbar onSearchHandler={onSearchHandler} />
      <div className="px-10">
        {isSearched ? (
          <>
            <h1>Search Result - "{searchQuery}" </h1>
            <div className="grid grid-cols-3 gap-10">
              {searchVideoList.map((video, index) => {
                console.log(video);
                return (
                  <Link to={`/videos/${video.bucket_id}`} key={index}>
                    <div className=" w-fit rounded-md bg-red border">
                      <div
                        className={`w-[440px] h-[260px] bg-red-500 bg-cover`}
                      >
                        <img className="h-full w-full" src={video.thumbnail} />
                      </div>
                      <div className="px-5 py-5">
                        <h1 className="font-semibold ">{video.title}</h1>
                      </div>
                    </div>
                  </Link>
                );
              })}
            </div>
          </>
        ) : (
          <>
            <h5 className="text-[#4a4a4a] text-lg font-normal mb-4">
              All Videos
            </h5>
            <div className="grid grid-cols-3 gap-10">
              {videoList.map((video, index) => {
                console.log(video.thumbnail);
                return (
                  <Link to={`/videos/${video.bucket_id}`} key={index}>
                    <div className=" w-fit rounded-md bg-red border">
                      <div
                        className={`w-[440px] h-[260px] bg-red-500 bg-cover`}
                      >
                        <img className="h-full w-full" src={video.thumbnail} />
                      </div>
                      <div className="px-5 py-5">
                        <h1 className="font-semibold ">{video.title}</h1>
                      </div>
                    </div>
                  </Link>
                );
              })}
            </div>
          </>
        )}
      </div>
    </>
  );
}

export default Home;
