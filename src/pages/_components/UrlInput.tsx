import { MdAddCircleOutline } from "react-icons/md";
import { FaRegTrashAlt } from "react-icons/fa";

interface UrlInputProps {
  url: string;
  index: number;
  onUrlChange: (index: number, value: string) => void;
  onAddUrl: () => void;
  onRemoveUrl: (index: number) => void;
  isRemovable: boolean;
}

const UrlInput: React.FC<UrlInputProps> = ({
  url,
  index,
  onUrlChange,
  onAddUrl,
  onRemoveUrl,
  isRemovable,
}) => {
  return (
    <div style={{ marginBottom: "10px" }}>
      <div className="flex items-center gap-3">
        <input
          type="text"
          placeholder={`Enter TikTok URL #${index + 1}`}
          value={url}
          onChange={(e) => onUrlChange(index, e.target.value)}
          required
          style={{ width: "100%", padding: "8px", fontSize: "14px" }}
          className="border border-gray-300 rounded"
        />
        <button type="button" onClick={onAddUrl}>
          <MdAddCircleOutline size={30} />
        </button>
        <button
          type="button"
          onClick={() => onRemoveUrl(index)}
          disabled={!isRemovable}
        >
          <FaRegTrashAlt size={25} />
        </button>
      </div>
    </div>
  );
};

export default UrlInput;
