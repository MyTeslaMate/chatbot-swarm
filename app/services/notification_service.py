def send_email(email_address, message):
    response = f"Email sent to: {email_address} with message: {message}"
    return {"response": response}

def submit_ticket(description):
    return {"response": f"Ticket created for {description}"}
