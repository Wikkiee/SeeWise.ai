import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../api";

function Player({ bucketId }) {
  const [videoSource, setVideoSource] = useState(null);
  const [bId, setBId] = useState("");
  const { bucket_id } = useParams();

  useEffect(() => {
    api.get(`api/videos/get/${bucket_id}/`).then((response) => {
      console.log(response);
      setVideoSource(response.data);
    });
    console.log(videoSource);
  }, []);

  return (
    <div>
      <div className="w-full bg-white shadow-custom  px-20 py-6 mb-5">
        <div>
          <strong>SeeWise</strong>
        </div>
      </div>
      <Link className="font-light text-gray-500 text-sm mb-12 ml-20 " to={"/"}>
        Back
      </Link>
      {videoSource ? (
        <>
          <div className="h-screen w-full flex justify-center mt-2 flex-col items-center">
            <video className="w-[1080px] h-[450px]" width="1080" controls>
              <source src={videoSource.url} type="video/mp4" />
              Your browser does not support the video tag.
            </video>
            <div className="w-full text-center mt-8">
              <h1 className="font-semibold">{videoSource.title}</h1>
            </div>
          </div>
        </>
      ) : (
        <h1> Loading</h1>
      )}
    </div>
  );
}
export default Player;
