import imageio

def extract_frames(video_path, output_path):
    # Open the video file
    reader = imageio.get_reader(video_path)

    # Get frames per second (fps) and frame count
    fps = reader.get_meta_data()['fps']
    frame_count = reader.count_frames()

    # Specify the format for naming the frames 
    frame_name_format = output_path + "/3-10_data-{:04d}.png"

    # Loop through each frame and save it
    for frame_number in range(0, frame_count, 2):
        frame = reader.get_data(frame_number)

        # Save the frame
        frame_filename = frame_name_format.format(frame_number)
        imageio.imwrite(frame_filename, frame)

if __name__ == "__main__":
    # Specify the input video path
    input_video_path = r"C:\\SP24\\EGR402 Capstone\\Data set training videos\\3-10_video.mp4"

    # Specify the output directory for frames
    output_directory = "C:\\SP24\\EGR402 Capstone\\Data set training videos\\3-10_frames"

    # Call the function to extract frames
    extract_frames(input_video_path, output_directory)