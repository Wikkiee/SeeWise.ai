import { Link } from "react-router-dom";
import videoEdit from "../assets/videoEdit.svg";
import "../styles/Navbar.css";

function Navbar({ onSearchHandler }) {
  return (
    <div className="mb-10">
      <nav>
        <ul>
          <li>
            <div>
              <strong>SeeWise</strong>
              <input
                placeholder="Search Title"
                onChange={(event) => {
                  onSearchHandler(event);
                }}
              ></input>
            </div>
          </li>
          <li>
            <Link to={"/user"}>
              <div>
                <img src={videoEdit} />

                <strong>My Videos</strong>
              </div>
            </Link>
          </li>
        </ul>
      </nav>
    </div>
  );
}
export default Navbar;
