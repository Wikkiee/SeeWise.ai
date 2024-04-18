import { useEffect, useState } from "react";
import { storage } from "../firebase";
import ReactPlayer from "react-player";
import {
  ref,
  uploadBytes,
  getDownloadURL,
  deleteObject,
} from "firebase/storage";
import { v4 } from "uuid";
import api from "../api";
import { Link } from "react-router-dom";
function User() {
  const [title, setTitle] = useState("");
  const [videoUpload, setVideoUpload] = useState(null);
  const [thumbnailUpload, setThumbnailUpload] = useState(null);
  const [videoList, setVideoList] = useState([]);
  const [editingTitleId, setEditingTitleId] = useState(null);
  const [newTitle, setNewTitle] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const uploadVideo = () => {
    setIsUploading(true);
    if (title == null || videoUpload == null) {
      alert("Please Enter the Title / Select the video file");
      return;
    }
    const identifier = v4();
    const videoRef = ref(storage, `videos/${identifier}`);
    const thumbnailRef = ref(storage, `images/${identifier}`);
    uploadBytes(videoRef, videoUpload).then((snapshots) => {
      getDownloadURL(snapshots.ref)
        .then((url) => {
          const videoUrl = url;
          uploadBytes(thumbnailRef, thumbnailUpload).then((snapshots) => {
            getDownloadURL(snapshots.ref).then((url) => {
              const thumbnailUrl = url;
              api
                .post("/api/videos/retrive-and-upload/", {
                  title: title,
                  url: videoUrl,
                  thumbnail: thumbnailUrl,
                  bucket_id: identifier,
                })
                .then((response) => {
                  console.log(response);
                  setIsUploading(false);
                  setVideoList((prev) => [...prev, response.data]);
                })
                .catch((error) => {
                  console.log(error);
                });
            });
          });
        })
        .catch((error) => {
          console.log(error);
        });
    });
  };

  const deleteVideo = (id, bucket_id) => {
    api
      .delete(`api/videos/delete/${id}/`)
      .then((response) => {
        if (response.status == 204) {
          const videoRef = ref(storage, `videos/${bucket_id}`);
          const thumbnailRef = ref(storage, `images/${bucket_id}`);
          deleteObject(videoRef)
            .then(() => {
              console.log("Video deleted successfully");
            })
            .catch((error) => {
              console.error("Error deleting file:", error);
            });
          deleteObject(thumbnailRef)
            .then(() => {
              console.log("Thumbnail deleted successfully");
            })
            .catch((error) => {
              console.error("Error deleting file:", error);
            });
          setVideoList(() => {
            return videoList.filter((video) => {
              return video.id != id;
            });
          });
        }
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const editTitleHandler = (id) => {
    api
      .put(`api/videos/update/${id}/`, { title: newTitle })
      .then((response) => {
        if (response.status == 200) {
          setVideoList(() => {
            const newVideoList = videoList.filter((video) => {
              return video.id != id;
            });
            newVideoList.push(response.data);
            return newVideoList;
          });
        }
      });
  };

  useEffect(() => {
    api.get("api/videos/retrive-and-upload/").then((response) => {
      console.log(response);
      setVideoList(response.data);
    });
  }, []);

  return (
    <div>
      <div className="w-full bg-white shadow-custom  px-20 py-6 mb-5">
        <div>
          <strong>SeeWise</strong>
        </div>
      </div>
      <div className="px-12">
        <Link className="font-light text-gray-500 text-sm mb-12 " to={"/"}>
          Back
        </Link>
        <div className="mt-10">
          <div className="w-full flex flex-col justify-center items-center">
            <input
              type="text"
              placeholder="Enter the Title"
              className="px-2 py-2 border rounded w-[25rem] mb-5 border-black"
              onChange={(event) => {
                setTitle(event.target.value);
              }}
            />
            <label for="files">Open a Video File</label>

            <input
              id="files"
              type="file"
              accept="video/*"
              className="mb-5"
              onChange={(event) => {
                setVideoUpload(event.target.files[0]);
              }}
            />
            <label for="files">Select a thumbnail</label>

            <input
              type="file"
              accept=".png, .jpeg, .jpg"
              className="mb-5"
              onChange={(event) => {
                setThumbnailUpload(event.target.files[0]);
              }}
            />
            <button
              className="bg-black text-white px-10 py-2 rounded"
              onClick={uploadVideo}
            >
              Upload
            </button>
            <br></br>
            {isUploading ? <span> Uploading ...</span> : null}
          </div>
          <div>
            <div>
              <div className="w-full">
                <h1 className="font-semibold">My Videos</h1>
                <hr className="my-3"></hr>
              </div>
              <>
                {videoList.map((video, index) => (
                  <div className="mb-10" key={index}>
                    <h1>
                      {editingTitleId === video.id ? (
                        <input
                          type="text"
                          className="px-2 py-2 border rounded w-[25rem]  border-black"
                          value={newTitle !== null ? newTitle : video.title}
                          onChange={(e) => {
                            setNewTitle(e.target.value);
                          }}
                        />
                      ) : (
                        <span className="font-semibold text-sm ">
                          {video.title}
                        </span>
                      )}
                    </h1>
                    <ReactPlayer url={video.url} controls />
                    <br></br>
                    <button
                      className="border-none bg-red-600 text-white border px-5 py-2 rounded font-medium text-sm  mx-4"
                      onClick={() => {
                        deleteVideo(video.id, video.bucket_id);
                      }}
                    >
                      Delete
                    </button>

                    {editingTitleId === video.id ? (
                      <button
                        className="border-black bg-white text-black border px-5 py-2 rounded font-medium text-sm mx-4"
                        onClick={() => {
                          setEditingTitleId(null);
                          editTitleHandler(video.id);
                        }}
                      >
                        Save Title
                      </button>
                    ) : (
                      <button
                        className="border-none bg-black text-white border px-5 py-2 rounded font-medium text-sm  mx-4"
                        onClick={() => setEditingTitleId(video.id)}
                      >
                        Edit Title
                      </button>
                    )}
                  </div>
                ))}
              </>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default User;
