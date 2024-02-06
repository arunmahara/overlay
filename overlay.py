from PIL import Image


def overlay_images(bg_path: str, ov_path: str, output_path: str) -> None:
    try:
        print(f"Overlaying {ov_path} on {bg_path} and saving to {output_path}")

        # Open the profile image
        profile = Image.open(bg_path)

        # Open the logo image
        logo = Image.open(ov_path)

        # Resize the logo to fit the profile image (adjust the resizing factor to make it bigger)
        logo_width, logo_height = logo.size
        profile_width, profile_height = profile.size
        logo_resized = logo.resize((int(profile_width), int(profile_height)))

        # Calculate paste coordinates from the left bottom corner
        paste_x = 0  # Left
        paste_y = profile_height - logo_resized.size[1]  # Bottom

        # Overlay the logo on the profile image
        profile.paste(logo_resized, (paste_x, paste_y), logo_resized)

        # Save the modified profile image
        profile.save(output_path)

        print(f"Overlayed successful to {output_path}")

    except Exception as e:
        raise e
