import click
import .dicom_utils


@click.command()
@click.option('--p_name', default='', help='Patient\'s name')
@click.option('--p_birth_date', default='', help='Patient\'s birth date')
@click.option('--p_sex', default='', help='Patient\'s sex')
@click.option('--set_datetime', default='N', help='Y/N sets content date and \
              time to current datetime')
@click.option('--add_age', default='N', help='Add patient\'s age at time of \
              scan')
@click.argument('item_name', help='The name of the file/folder to be \
                read/modified')             
def main(filefolder,p_name,p_birth_date,p_sex,set_datetime,add_age,item_name):
    #if 
    
if __name__=="__main__":
    main()