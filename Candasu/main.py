from website import create_app
import logging
app = create_app()

if __name__ == '__main__':
    # logging.basicConfig(filename='internship_logs.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
    # @app.route('/blogs')
 
    app.run(debug=True,port=5000)

       # def blog():
    #     app.logger.info('Info level log')
    #     app.logger.warning('Warning level log')
    #     return f"Welcome to the Blog"