from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

import cgi
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# create session and connect db
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind=engine)
session = DBsession()


class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/restaurants'):
                restaurants = session.query(Restaurant).all()
                output = ''
                self.send_response(200)
                self.send_header('Context-type', 'text/html')
                self.end_headers()
                output += "<html><body>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" %restaurant.id
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" %restaurant.id
                    output += "</br></br></br>"

                output += "</body></html>"
                self.wfile.write(output)
            if self.path.endswith('/restaurants/new'):
                self.send_response(200)
                self.send_header('Context-type', 'text/html')
                self.end_headers()

                output = "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder = 'New Restaurant Name' > "
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output)
            if self.path.endswith('/edit'):
                id_number = self.path.split('/')[2]
                print id_number
                myRestaurantQuery = session.query(Restaurant).filter_by(id=id_number).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Context-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>Update the old name:</h1>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/" + id_number + "/edit'>"
                    output += "<input name='updateRestaurantName' type='text' placeholder = '%s' > " % myRestaurantQuery.name
                    output += "<input type='submit' value='Update'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
            if self.path.endswith('/delete'):
                id_number = self.path.split('/')[2]
                print id_number
                myRestaurantQuery = session.query(Restaurant).filter_by(id=id_number).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Context-type', 'text/html')
                    self.end_headers()

                    output = "<html><body>"
                    output += "<h1>Do you want to delete the restaurnt: %s?</h1>" % myRestaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/" + id_number + "/delete'>"
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(output)
                    return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith('/restaurants/new'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                print ctype
                print pdict
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    print fields
                    messagecontent = fields.get('newRestaurantName')
                    # create a new Restaurant obj
                    newRestaurant = Restaurant(name=messagecontent[0])
                    session.add(newRestaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Context-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

            if self.path.endswith('/edit'):
                id_number = self.path.split('/')[2]
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('updateRestaurantName')

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=id_number).one()
                    if myRestaurantQuery !=[]:

                        myRestaurantQuery.name = messagecontent[0]
                        session.add(myRestaurantQuery)
                        session.commit()

                        self.send_response(301)
                        self.send_header('Context-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                        return
            if self.path.endswith('/delete'):
                id_number = self.path.split('/')[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=id_number).one()
                if myRestaurantQuery != []:
                    session.delete(myRestaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Context-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return
        except:
            pass


def main():
    try:
        port = 11111
        server = HTTPServer(('', port), webServerHandler)
        print 'Web server running...open localhost:%s/restaurants in your browser' % port
        server.serve_forever()
    except KeyboardInterrupt:
        print '^C received, shutting down server'
        server.socket.close()


if __name__ == '__main__':
    main()
