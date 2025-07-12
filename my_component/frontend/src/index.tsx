import { createRoot } from "react-dom/client"
import AnnotatedText from "./annotated-text"

const container = document.getElementById("root")
const root = createRoot(container!)
root.render(<AnnotatedText />)
