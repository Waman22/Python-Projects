# Import the qrcode library for generating QR codes
import qrcode

'''This code generates a QR code based on user-provided information, including the department, tool type, and entry date.
Functionality:
The generate_qr_code function creates a QR code using the qrcode library. It takes two parameters: data_type (to name the QR code file) and data (the content to be encoded in the QR code).
The QR code is configured with specific parameters such as version, error correction level, box size, and border thickness.
The generated QR code is saved as a PNG file with a filename that includes the data type.'''

def generate_qr_code(data_type, data):
    """Generates a QR code based on the provided data type and data."""
    # Create a QRCode object with specified parameters
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR Code (1 to 40)
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Error correction level
        box_size=10,  # Size of each box in the QR code grid
        border=4,  # Thickness of the border (minimum is 4)
    )
    
    # Add the data to the QR code
    qr.add_data(data)
    qr.make(fit=True)  # Adjust the QR code size to fit the data

    # Create an image from the QR code
    img = qr.make_image(fill_color="green", back_color="white")
    
    # Save the generated QR code image to a file
    img.save(f"qr_code_{data_type}.png")
    print(f"QR code for {data_type} saved as 'qr_code_{data_type}.png'.")

# Main program
def main():
    print("QR Code Generator")
    
    # Get user input for the data type and other details
    data_type = input("Enter the data type: ")  # Make data_type flexible
    department = input("Enter the department: ")
    tool = input("Enter the type of tool: ")
    date = input("Enter the entry date: ")
    
    # Format the data to be encoded in the QR code
    data = f"Department: {department} workshop, \n Tool: {tool}\n Date: {date}"
    
    # Generate the QR code with the provided data
    generate_qr_code(data_type, data)

# Entry point of the program
if __name__ == "__main__":
    main()