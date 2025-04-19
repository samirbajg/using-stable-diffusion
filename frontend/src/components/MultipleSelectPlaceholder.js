import * as React from 'react';
import { useTheme } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import FormControl from '@mui/material/FormControl';

const MultipleSelectPlaceholder = ({ onRoomSelect }) => {
  const theme = useTheme();
  const [selectedRoom, setSelectedRoom] = React.useState('');
  const [error, setError] = React.useState('');

  const handleChange = (event) => {
    const value = event.target.value;
    setSelectedRoom(value);

    if (!value) {
      setError('give room type');
      return;
    }

    if (!value.toLowerCase().includes('room')) {
      setError('provide valid room');
      return;
    }

    setError('');
    onRoomSelect(value);
  };


  return (
    <FormControl sx={{ m: 1, width: 300, mt: 3 }}>
      <TextField
        value={selectedRoom}
        onChange={handleChange}
        placeholder="Enter a room name (e.g. Living Room)"
        error={!!error}
        helperText={error}
        fullWidth
        label="Room Name"
        variant="outlined"
      />
    </FormControl>
  );
};

export default MultipleSelectPlaceholder;
