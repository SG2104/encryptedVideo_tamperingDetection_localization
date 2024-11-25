from graphviz import Digraph

# Create a new directed graph
dot = Digraph(comment='System Design Diagram')

# Add nodes
dot.node('A', 'User')
dot.node('B', 'Encryption Module')
dot.node('C', 'Cloud Storage (AWS S3)')
dot.node('D', 'Cloud Processing (AWS Lambda)')
dot.node('E', 'Notification System')
dot.node('F', 'User Interface (Optional)')

# Add edges
dot.edge('A', 'B', 'Upload raw video')
dot.edge('B', 'C', 'AES encryption\nSHA-256 hash generation\nWatermark embedding')
dot.edge('C', 'D', 'Retrieve data')
dot.edge('D', 'E', 'Tampering detection and localization')
dot.edge('E', 'A', 'Alert')
dot.edge('E', 'F', 'Optional: Visualize tampering logs')

# Render the diagram to a file
dot.render('system_design_diagram.gv', view=True)