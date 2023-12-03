from pytube import YouTube
import os

while True:
    try:
        video_url = input("Enter the Youtube url(-1 for exit): ")
        if video_url == '-1':
            break
        elif "https://www.youtube.com/watch?v=" in video_url:
            yt = YouTube(video_url)
            print("Valid YouTube URL\n")
        else:
            raise ValueError("Invalid YouTube URL")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        print()
        continue     
        
    # Kullanıcıya MP3 veya MP4 formatını sormak
    while True:
        format_choice = input("Do you want to download in MP3 or MP4 format? (Enter 'mp3' or 'mp4'): ").lower()
        if format_choice in ['mp3', 'mp4']:
            break
        print("Invalid format seleceted !!!\n")

    video_name = f"{yt.title}.{format_choice}"

    # Kullanıcıya indirme konumunu sormak
    download_path = input("\nEnter the download path (or press enter to save in the current directory): ")

    # Eğer download_path belirtilmediyse, programın çalıştığı dizine kaydet
    if not download_path:
        download_path = os.getcwd()
    elif not os.path.exists(download_path):
        print(f"\nThe path '{download_path}' does not exist. Saving in the current directory.\n")
        download_path = os.getcwd()

    # MP3 formatını seçtiyse sadece sesi indir
    if format_choice == 'mp3':
        audio_stream = yt.streams.filter(only_audio = True).first()
        audio_stream.download(output_path = download_path, filename = video_name)
        print("\nAudio downloaded successfully!\n")

    # MP4 formatını seçtiyse mevcut formatları gösterin ve seçim yapmasını isteyin
    else:
        while True:
            print("\nAvailable formats: ")
            for i, stream in enumerate(yt.streams.filter(progressive = True, file_extension = 'mp4')):
                filesize_in_bytes = stream.filesize
                filesize_in_mb = filesize_in_bytes / (1024 * 1024)  # Byte'ı MB'a çevirme
                filesize_in_gb = filesize_in_bytes / (1024 * 1024 * 1024)  # Byte'ı GB'a çevirme
                print(f"{i+1}. Resolution: {stream.resolution}, Format: {stream.mime_type} , Filesize: {filesize_in_mb:.2f} MB") 
            try:
                selection = int(input("\nEnter the number of the desired format: ")) - 1
                if 0 <= selection < len(yt.streams.filter(progressive = True, file_extension='mp4')):
                    print("\nDownload has been started. Don't close the program until download finish succesfully!")
                    selected_stream = yt.streams.filter(file_extension='mp4')[selection]
                    selected_stream.download(output_path=download_path, filename=video_name)
                    print("Video downloaded successfully!\n")
                    break
                else:
                    print("Invalid selection!\n")
            except ValueError:
                print("Please enter a valid number.\n")
            except Exception as e:
                print(f"An error occurred: {e}\n")

